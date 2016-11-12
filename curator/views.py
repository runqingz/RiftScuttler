from django.db import connection
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import *
from .helpers import *


# Create your views here.
# http://maxivak.com/executing-raw-sql-in-django/
# https://docs.djangoproject.com/en/dev/topics/forms/#form-objects
# dynamic SQL: http://stackoverflow.com/questions/8320136/django-raw-sql-queries-with-a-dynamic-number-of-variables
# Get current URL: http://stackoverflow.com/questions/3248682/django-get-url-of-current-page-including-parameters-in-a-template
# TODO: authentication and error handling


def add_data_page(request):
    if request.user.is_staff or request.user.is_superuser:
        cursor = connection.cursor()
        table = check_page_and_return_table(request)
        if request.method == 'POST':
            form = AccessFormInput(request.POST, extra=table.cols)
            if form.is_valid():
                for (attribute, value) in form.extra_attributes():
                    table.args.append([attribute, value])
                table.args = reorder_dictionary(table)
                insert_data(cursor, table)
                name = create_reverse_name_add(table.tname)
                return redirect(reverse(name), permanent=True)
        form = AccessFormInput(extra=table.cols)
        list_of_data = select_data(cursor, table.tname)
        args = get_args(table.cols)
        context = create_context(table.tname, form, list_of_data, args)
        return render(request, 'curator/add.html', context)
    else:
        return redirect(login_page, permanent=True)


def remove_data_page(request):
    if request.user.is_staff or request.user.is_superuser:
        cursor = connection.cursor()
        table = check_page_and_return_table(request)
        if request.method == 'POST':
            form = AccessFormInput(request.POST, extra=table.pk)
            if form.is_valid():
                for (attribute, value) in form.extra_attributes():
                    table.args.append([attribute, value])
                table.args = reorder_dictionary(table)
                delete_data(cursor, table)
                name = create_reverse_name_remove(table.tname)
                return redirect(reverse(name), permanent=True)
        form = AccessFormInput(extra=table.pk)
        list_of_data = select_data(cursor, table.tname)
        args = get_args(table.cols)
        context = create_context(table.tname, form, list_of_data, args)
        return render(request, 'curator/remove.html', context)
    else:
        return redirect(login_page, permanent=True)


def edit_data_page(request):
    if request.user.is_staff or request.user.is_superuser:
        cursor = connection.cursor()
        table = check_page_and_return_table(request)
        if request.method == 'POST':
            form = AccessFormInput(request.POST, extra=table.cols)
            if form.is_valid():
                for (attribute, value) in form.extra_attributes():
                    table.args.append([attribute, value])
                table.args = reorder_dictionary(table)
                table.non_pk_args = get_non_pk_args(table)
                edit_data(cursor, table)
                name = create_reverse_name_edit(table.tname)
                return redirect(reverse(name), permanent=True)
        form = AccessFormInput(extra=table.cols)
        list_of_data = select_data(cursor, table.tname)
        args = get_args(table.cols)
        context = create_context(table.tname, form, list_of_data, args)
        return render(request, 'curator/edit.html', context)
    else:
        return redirect(login_page, permanent=True)


def login_page(request):
    context = {
        "welcome": "You should login.",
    }
    return render(request, "curator/login.html", context)


def curator_home(request):
    if request.user.is_staff or request.user.is_superuser:
        context = {
            "welcome": "Welcome to the curator's home page.",
        }
    else:
        context = {
            "welcome": "You are not authorized to view this page.",
        }
    return render(request, "curator/index.html", context)

# Create navigation bar for home page