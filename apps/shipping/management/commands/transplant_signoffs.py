# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is l10n django site.
#
# The Initial Developer of the Original Code is
# Mozilla Foundation.
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****

'''Bring sign-offs from a stable branch onto a project branch.
'''

from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from shipping.models import AppVersion
from shipping.api import accepted_signoffs
import pdb

class Command(BaseCommand):
    option_list = BaseCommand.option_list
    help = 'Transplant Signoffs and Actions from one appver to the other'
    args = 'old-appver new-appver'

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError, "two arguments required, old and new appversion"
        old = AppVersion.objects.get(code=args[0])
        new = AppVersion.objects.get(code=args[1])
        if old.tree.l10n != new.tree.l10n:
            raise CommandError, "Old and new appversion don't share l10n"
        sos = accepted_signoffs(id=old.id)
        for so in sos:
            print "transplanting " + so.locale.code
            _so = new.signoffs.create(push = so.push,
                                      author = so.author,
                                      when = so.when,
                                      locale = so.locale)
            for a in so.action_set.order_by('pk'):
                _so.action_set.create(flag = a.flag,
                                      author = a.author,
                                      when = a.when,
                                      comment = a.comment)
