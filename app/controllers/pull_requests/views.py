# -*- coding: utf-8 -*-

#
# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2 License.
#
# This product includes software developed at Datadog
# (https://www.datadoghq.com/).
#
# Copyright 2018 Datadog, Inc.
#

"""pull_requests/views.py

pull request related routes and view-specific logic.
"""

from flask import render_template, request
from flask_login import login_required
from . import pull_request
from ...models import Repo, PullRequest


@pull_request.route('/<int:id>', methods=['GET'])
@login_required
def index(id):
    """
    Displays pull_requests opened by external contributors related to a
    repository.
    """
    repo = Repo.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)

    pagination = repo.pull_requests.order_by(PullRequest.timestamp.asc()) \
                                   .paginate(
        page, per_page=10, error_out=False
    )
    pull_requests = pagination.items

    return render_template(
        'pull_requests.html',
        repo=repo,
        pull_requests=pull_requests,
        pagination=pagination
    )
