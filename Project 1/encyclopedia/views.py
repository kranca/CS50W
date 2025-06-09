from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

import markdown
import random
import re

from . import util

def clean_string(text):
    return re.sub(r'[^A-Za-z0-9]', '', text.split('.')[0])

def render_valid_entry(request, content, entry=None):
    html_content = markdown.markdown(content)
    return render(request, "encyclopedia/title.html", {
            "content" : html_content,
            "entry" : entry
        })

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries" : util.list_entries()
    })

def get_entry(request, entry):
    content = util.get_entry(entry)
    
    if content:
        return render_valid_entry(request, content, entry)
    else:
        return render(request, "encyclopedia/error.html", {
            "content" : f"ERROR: Entry '{entry}' not found.",
            "entry" : entry
        })

    
def search_entry(request):
    if request.method == "GET":
        entry = request.GET.get("q", "")
        content = util.get_entry(entry)
        if content:
            return render_valid_entry(request, content)
        else:
            similar_entries = [item for item in util.list_entries() if entry.lower() in item.lower()]
            return render(request, "encyclopedia/search.html", {
                "content" : f"No entries match search for '{entry}'.",
                "similar_entries" : similar_entries,
                "search_keyword" : entry
            })
        
def get_random_entry(request):
    entry = random.choice(util.list_entries())
    content = util.get_entry(entry)
    if content:
            return render_valid_entry(request, content)
    else:
        return render(request, "encyclopedia/error.html", {
            "content" : f"Something went wrong: Entry '{entry}' not found."
        })
    
def new_page(request):
    if request.method == "POST":
        new_title = request.POST["new_title"]
        clean_title = clean_string(new_title)
        new_content = request.POST["new_content"]
        
        if clean_title.lower() in [entry.lower() for entry in util.list_entries()]:
            if clean_title != new_title:
                new_title += f" ({clean_title})"
            return render(request, "encyclopedia/error.html", {
                "content" : f"Entry '{new_title}' already exists. Please edit existing entry or create a new entry."
            })
        elif new_title == "":
            return render(request, "encyclopedia/error.html", {
                "content" : "Title can't be empty nor contain spaces, symbols or special characters.",
                "entry" : None
            })
        else:
            util.save_entry(clean_title, new_content)
            return get_entry(request, clean_title)
    else:
        return render(request, "encyclopedia/new_page.html")
    
def edit_page(request, entry):
    if request.method == "POST":
        new_content = request.POST["new_content"]
        util.save_entry(entry, new_content)
        return get_entry(request, entry)
        # return HttpResponseRedirect(reverse("get_entry", args=(entry,)))
    else:
        content = util.get_entry(entry)
        return render(request, "encyclopedia/edit_page.html", {
            "entry" : entry,
            "content" : content
        })