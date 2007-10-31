#!/usr/bin/python
#
# CDDL HEADER START
#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License (the "License").
# You may not use this file except in compliance with the License.
#
# You can obtain a copy of the license at usr/src/OPENSOLARIS.LICENSE
# or http://www.opensolaris.org/os/licensing.
# See the License for the specific language governing permissions
# and limitations under the License.
#
# When distributing Covered Code, include this CDDL HEADER in each
# file and include the License file at usr/src/OPENSOLARIS.LICENSE.
# If applicable, add the following below this CDDL HEADER, with the
# fields enclosed by brackets "[]" replaced with your own identifying
# information: Portions Copyright [yyyy] [name of copyright owner]
#
# CDDL HEADER END
#

#
# Copyright 2007 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#

"""Action describing a package dependency.

This module contains the DependencyAction class, which represents a
relationship between the package containing the action and another package.
"""

import urllib
import generic

class DependencyAction(generic.Action):
        """Class representing a dependency packaging object.  The fmri attribute
        is expected to be the pkg FMRI that this package depends on.  The type
        attribute is one of

        require - dependency is needed for correct function
        incorporate - require and freeze at specified version
        optional - dependency if present activates additional functionality,
                   but is not needed
        exclude - package non-functional if dependent package is present"""

        name = "depend"
        attributes = ("type", "fmri")
        key_attr = "fmri"

        def __init__(self, data=None, **attrs):
                generic.Action.__init__(self, data, **attrs)

        def generate_indices(self):
                # XXX Probably need to do something for other types, too.
                if self.attrs["type"] != "require":
                        return {}

                fmri = self.attrs["fmri"]

                # XXX Ideally, we'd turn the string into a PkgFmri, and separate
                # the stem from the version, or use get_dir_path, but we can't
                # create a PkgFmri without supplying a build release and without
                # it creating a dummy timestamp.  So we have to split it apart
                # manually.
                #
                # XXX This code will need to change once we start using fmris
                # with authorities.
                if fmri.startswith("pkg:/"):
                        fmri = fmri[5:]
                # Note that this creates a directory hierarchy!
                fmri = urllib.quote(fmri, "@").replace("@", "/")

                return {
                    "depend": fmri
                }
