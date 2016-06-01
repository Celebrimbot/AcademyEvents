"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.shortcuts import redirect
from app.forms import ContactForm, SchoolSelector, TrustSelector
from app.edudata import *
from datetime import datetime



# needed for handling data in detail views
import pandas

def school(request, urn):
    """Render details for a particular trust"""
    assert isinstance(request, HttpRequest)

    ## The aim here is to build a model of the School in a SchoolHistory object.
    ## This will give the urn, upin, school name, open date and closed date (if known)
    ## As well as all of the trusts, with their inc and dis dates, transfer in and out dates.
    ## and, of course, their URL

    # OK lets get some data...
    df = pandas.read_csv('C:\\Users\\physi_000\\documents\\visual studio 2015\\Projects\\AcademyEvents\\AcademyEvents\\app\\Academy Relationships.csv')

    school_events = df.ix[df['MasterURN']==int(urn),['Academy name','MasterUPIN','MasterURN','MasterDateOpened','MasterDateClosed','Transfer In', 'Transfer Out', 'Trust Name', 'Trust Company Number', 'Trust Incorporation Date', 'Trust Dissolution Date']]

    school_events.reset_index(level=0, inplace=True, drop=True)

    

    # Build a list of relationships
    relationships = []
    for i in range(0, school_events.shape[0]):
        row = school_events.iloc[i]
        
        args = {'name':row['Trust Name'], 'coho':row['Trust Company Number'],'incdate':row['Trust Incorporation Date']}
        if pandas.notnull(row['Transfer In']):    
            args.update(tin = row['Transfer In'])
        if pandas.notnull(row['Transfer Out']):    
            args.update(tout = row['Transfer Out'])

        relationships.append(RelationshipToTrust(**args))
    
    # prepare constructor arguments for SchoolHistory
    args = {'URN': urn, 'schoolName': school_events.ix[0,'Academy name'], 'openDate': school_events.ix[0,'MasterDateOpened'], 'relationships': relationships }
    if pandas.notnull(school_events.ix[0,'MasterDateClosed']):
        args.update(closedDate = school_events.ix[0,'MasterDateClosed'])
    
    # And the piece of resistance:
    sh = SchoolHistory(**args)

    return render(
        request,
        'app/school.html',
        context_instance = RequestContext(request,
        {
            'title':sh.schoolName + " (" + urn +")",
            'message':'Trust details below',
            'year':datetime.now().year,
            'sh':sh
        })
    )

def trust(request, coho_number):
    """Render details for a particular trust"""
    assert isinstance(request, HttpRequest)

    ## The aim here is to build a model of the Trust in a TrustHistory object.
    ## This will give the company number, trust name, incorporation date, dissolution date (if known)
    ## As well as all of the schools, with their open and close dates, transfer in and out dates.
    ## and, of course, their URL

    # OK lets get some data on trusts
    df = pandas.read_csv('C:\\Users\\physi_000\\documents\\visual studio 2015\\Projects\\AcademyEvents\\AcademyEvents\\app\\Academy Relationships.csv')

    trust_events = df.ix[df['Trust Company Number']==int(coho_number),['Academy name','MasterUPIN','MasterURN','MasterDateOpened','MasterDateClosed','Transfer In', 'Transfer Out', 'Trust Name', 'Trust Incorporation Date', 'Trust Dissolution Date']]

    trust_events.reset_index(level=0, inplace=True, drop=True)

    # Build a list of relationships
    relationships = []
    for i in range(0, trust_events.shape[0]):
        row = trust_events.iloc[i]
        
        args = {'name':row['Academy name'],'opendate':row['MasterDateOpened']}
        if pandas.notnull(row['Transfer In']):    
            args.update(tin = row['Transfer In'])
        if pandas.notnull(row['Transfer Out']):    
            args.update(tout = row['Transfer Out'])
        if pandas.notnull(row['MasterURN']):    
            args.update(URN = row['MasterURN'])

        relationships.append(RelationshipToSchool(**args))
    
    # prepare constructor arguments for TrustHistory
    args = {'companyNumber': coho_number, 'trustName': trust_events.ix[0,'Trust Name'], 'incorporationDate': trust_events.ix[0,'Trust Incorporation Date'], 'relationships': relationships }
    if pandas.notnull(trust_events.ix[0,'Trust Dissolution Date']):
        args.update(dissolutionDate = trust_events.ix[0,'Trust Dissolution Date'])
    
    # And the piece of resistance:
    th = TrustHistory(**args)

    # Now get some FMGS data.  This means first finding any returns submitted by this trust.
    df = pandas.read_csv('C:\\Users\\physi_000\\documents\\visual studio 2015\\Projects\\AcademyEvents\\AcademyEvents\\app\\FMGSReturn.txt')

    fmgs_events = df.ix[df['Company number']==int(coho_number),["Date Created","Reference","FormReturnType","other_comments"]]
    fmgs_events.reset_index(level=0, inplace=True, drop=True)

    # print(fmgs_events)

    returns = []
    for i in range(0, fmgs_events.shape[0]):
        row = fmgs_events.iloc[i]
        
        
        return_args = {'reference':row['Reference'].strip(),'subdate':row['Date Created']}

        
        # Only look for answers if necessary:
        if row.FormReturnType == "Existing MAT" or row.FormReturnType == "New MAT, previous FMGS":
            return_args.update(type = "AA")
        else:
            return_args.update(type = "FMGS")
            df = pandas.read_csv('C:\\Users\\physi_000\\documents\\visual studio 2015\\Projects\\AcademyEvents\\AcademyEvents\\app\\FMGSAnswer.txt')
        
            fmgs_answers = df.ix[df['Reference']==row.Reference,["QNum","Answer","TargetDate","ActionPlan"]]
            fmgs_answers.reset_index(level=0, inplace=True, drop=True)

            print(fmgs_answers)
            
            answers = []
            for j in range(0, fmgs_answers.shape[0]):
                answer = fmgs_answers.iloc[j]

                args = {'questionnumber':answer['QNum'],'answer':answer['Answer']}
                if answer['Answer'] == "no":
                    args.update(targetdate = answer['TargetDate'])
                    args.update(actionplan = answer['ActionPlan'])

                answers.append(FMGSAnswer(**args))

            return_args.update(answers = answers)
            

        th.addFMGS(FMGS(**return_args))


    # Then it means checking for school coverage


    # For now lets fake it to test the python data model:
        
    return render(
        request,
        'app/trust.html',
        context_instance = RequestContext(request,
        {
            'title':th.trustName + " (" + coho_number +")",
            'message':'Trust details below',
            'year':datetime.now().year,
            'th':th
        })
    )

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    
    trust_selection = TrustSelector
    school_selection = SchoolSelector

    if request.method == 'POST':
        trust = trust_selection(data=request.POST)
        
        if trust.is_valid() and not request.POST.get(
                'trust_number'
            , '') == '':
            next_url = 'trust/' + request.POST.get(
                'trust_number'
            , '')
            
            return redirect(next_url)

        school = school_selection(data=request.POST)
        
        if school.is_valid():
            next_url = 'school/' + request.POST.get(
                'school_urn'
            , '')

            return redirect(next_url)

    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'trust': trust_selection,
            'school': school_selection
        })
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    
    form_class = ContactForm
    
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get(
                'contact_name'
            , '')
            contact_email = request.POST.get(
                'contact_email'
            , '')
            form_content = request.POST.get('content', '')

            #return redirect('contact')

    return render(
        request,
        'app/contact.html',
        context_instance = RequestContext(request,
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
            'form': form_class
        })
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
    )
