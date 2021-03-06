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

'''Views for the main navigation pages.
'''

from django.shortcuts import render_to_response, redirect
from django.utils.safestring import mark_safe
from django.template import RequestContext

from life.models import Locale


def index(request):
    from shipping.views import homesnippet as shipping_snippet
    from pushes.views import homesnippet as pushes_snippet
    from l10nstats.views import homesnippet as stats_snippet
    from bugsy.views import homesnippet as bugs_snippet

    shipping_div = mark_safe(shipping_snippet(request))
    pushes_div = mark_safe(pushes_snippet(request))
    l10nstats_div = mark_safe(stats_snippet(request))
    bugs_div = mark_safe(bugs_snippet(request))
    return render_to_response('homepage/index.html', {
            'shipping': shipping_div,
            'pushes': pushes_div,
            'l10nstats': l10nstats_div,
            'bugs': bugs_div,
            }, context_instance=RequestContext(request))


def teams(request):
    locs = Locale.objects.order_by('name')
    return render_to_response('homepage/teams.html', {
            'locales': locs,
            }, context_instance=RequestContext(request))


def locale_team(request, code):
    try:
        loc = Locale.objects.get(code=code)
    except Locale.DoesNotExist:
        return redirect('homepage.views.teams')

    from l10nstats.views import teamsnippet as stats_snippet
    l10nstats_div = mark_safe(stats_snippet(request, loc))

    from shipping.views import teamsnippet as ship_snippet
    ship_div = mark_safe(ship_snippet(request, loc))

    from bugsy.views import teamsnippet as bug_snippet
    bug_div = mark_safe(bug_snippet(request, loc))

    name = loc.name or loc.code

    return render_to_response('homepage/locale-team.html', {
            'locale': loc,
            'name': name,
            'l10nstats': l10nstats_div,
            'shipping': ship_div,
            'bugs': bug_div,
            }, context_instance=RequestContext(request))
