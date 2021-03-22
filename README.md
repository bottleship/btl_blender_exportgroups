# Blender alembic export groups

## Introduction

Exporting multiple sets of objects as alembic caches from Blender requires a lot of manual work, that has to be repeated on every export, especially if different object sets have different settings. There are nearly 30 settings, imagine having to set them to specific values multiple times on each export.

This addon solves the problem by persisting "groups" of objects, each group with its own export settings, in the scene.

## How to use

- Select the objects you would like to add to a group.
- From the "Alembic export group settings" tab in object view, click "Create group".
- Add objects to the group by selecting some objects and in the group's panel click "Add selected objects to export group".
- Set the export settings as needed.
- Select the group by clicking its checkbox, then click "Export selected groups".

## Installation

Install from the Blender menu:
- Go to Edit → Preferences and navigate to the Add-ons tab
- Select Install from the top
- Navigate to the addon location and open it
- Activate the addon

## How it works

A custom property `alembic_export_groups` is added to the scene.
This is a list of export groups.

Each export group contains a list of (pointers to) objects, and a complete set of alembic export settings.
