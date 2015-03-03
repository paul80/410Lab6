from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect

from main.models import Link
from main.models import Tag

@csrf_protect
def index(request):
	context=RequestContext(request)

	links=Link.objects.all()

	return render_to_response('main/index.html', {'links':links},context)

def tags(request):
	context = RequestContext(request)
	tags = Tag.objects.all()
	return render_to_response('main/tags.html', {'tags': tags}, context)

def tag(request, tag_name):
	context = RequestContext(request)
	the_tag = Tag.objects.get(name=tag_name)
	links = the_tag.link_set.all()
	return render_to_response('main/index.html', {'links': links, 'tag_name': '#' + tag_name}, context)

def add_link(request):
	context= RequestContext(request)
	if request.method =="POST":
		url=request.POST.get('url','')
		tags=request.POST.get('tags','')
		title= request.POST.get('title','')

		new_link= Link(title=title,url=url)
		#Many to many relationship 
		new_link.save()
		for tag in tags.split(','):
			try:
				new_link.tags.add(Tag.objects.get(name=tag))
			except:
				continue
		#new_link.save()
		#return redirect(index)
		new_link.save()

	return redirect(index)
	# return render(request, 'main/index.html', {})

# Create your views here.
#http://127.0.0.1:8000/bookmarks/