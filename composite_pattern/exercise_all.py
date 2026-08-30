"""
Problem: Permission System

You're building an authorization system for a company.

A user can be given:

Individual permissions

READ_USERS
CREATE_USERS
DELETE_USERS
VIEW_REPORTS
EXPORT_REPORTS

An individual permission should be able to answer:

permission.allows("READ_USERS")

But the company also wants Permission Groups.

For example:

USER_MANAGER
├── READ_USERS
├── CREATE_USERS
└── DELETE_USERS

And:

REPORT_MANAGER
├── VIEW_REPORTS
└── EXPORT_REPORTS

Groups can contain other groups.

For example:

ADMIN
├── USER_MANAGER
│   ├── READ_USERS
│   ├── CREATE_USERS
│   └── DELETE_USERS
│
└── REPORT_MANAGER
    ├── VIEW_REPORTS
    └── EXPORT_REPORTS

So:

Permission
    /       \
Individual   Group
             │
             ├── Permission
             ├── Permission
             └── Group
Requirements

Your system should allow:

admin.allows("READ_USERS")

→ True

admin.allows("EXPORT_REPORTS")

→ True

admin.allows("DELETE_DATABASE")

→ False

And:

report_manager.allows("VIEW_REPORTS")

→ True

The client should not care whether it's asking an individual permission or an entire permission group.

Implement it three ways
Version 1 — Classical

Use:

ABC
abstractmethod
Version 2 — Modern Python

Use:

Protocol

Don't use ABC.

Version 3 — Functional/procedural

No Composite class hierarchy.

You can use:

functions
dicts
lists
sets
recursion
"""