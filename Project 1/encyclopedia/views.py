from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

import markdown

from . import util

def render_valid_entry(request, content):
    html_content = markdown.markdown(content)
    return render(request, "encyclopedia/title.html", {
            "content" : html_content
        })

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries" : util.list_entries()
    })

def get_entry(request, entry):
    content = util.get_entry(entry)
    
    if content:
        return render_valid_entry(request, content)
    else:
        return render(request, "encyclopedia/title.html", {
            "content" : f"ERROR: Entry '{entry}' not found."
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