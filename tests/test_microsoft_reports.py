# -*- coding: utf-8 -*-
#
# Copyright (c) 2021, Ingram Micro
# All rights reserved.
#

from reports.nce_promos.entrypoint import generate


def test_nce_promos(progress, client_factory, response_factory, extra_context_callback):
    """
    Test dataset generation.
    To mock http calls, you must create the list of responses
    for each client call.

    Ex:
    ```

    responses = []
    # create a response for a count call

    responses.append(response_factory(count=100))

    # create response for a collection

    responses.append(response_factory(value=[
        {
            'id': 'OBJ-001',
            ....
        },
        {
            'id': 'OBJ-002',
            ....
        },
    ]))

    # create a response that raises an Exception

    responses.append(response_factory(exception=Exception('my_exception')))

    # create a response that returns a http 404

    responses.append(response_factory(status=404))

    # create a response and pass an RQL query, ordering and select
    # to check that it match

    responses.append(response_factory(
        query='in(status,(approved,rejected))',
        ordering=['-created'],
        select=['asset'],
        value=[],
    ))

    # create a client instance

    client = client_factory(responses)

    # create extra context information on the renderer used, if needed
    
    renderer_mock = mocker.MagicMock()
    renderer_mock.type = 'pdf'
    renderer_mock.render.return_value = 'outfile.pdf'
    renderer_mock.set_extra_context = extra_ctx_callback

    :param progress: MagicMock to use as progress_callback
    :type mocker: MagicMock
    :param client_factory: Function that returns an instance of ConnectClient
    :type client_factory: func
    :param response_factory: Function that creates ConnectClient reponses.
    :type response_factory: func
    :param extra_context_callback: Function that creates extra context information.
    :type extra_context_callback: func
    """

    pass
