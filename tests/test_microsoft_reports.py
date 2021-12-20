# -*- coding: utf-8 -*-
#
# Copyright (c) 2021, Ingram Micro
# All rights reserved.
#

from reports.nce_promos.entrypoint import generate, HEADERS

def test_nce_promos(progress, client_factory, response_factory, ff_request, tc_request):
    responses = []

    parameters = {
        'date': {
            'after': '2021-12-01T00:00:00',
            'before': '2021-12-20T00:00:00',
        },
        'product': {
            'all': True,
            'choices': [],
        },
        'mkp': {
            'all': True,
            'choices': [],
        },
    }

    responses.append(
        response_factory(
            query='ge(events.created.at,2021-12-01T00:00:00),le(events.created.at,2021-12-20T00:00:00),'
                  'eq(status,approved),eq(asset.params.id,nce_promo_final)',
            value=ff_request,
        ),
    )

    responses.append(
        response_factory(
            query='eq(product.id,PRD-111-222-333),eq(account.id,TA-1)',
            value=tc_request,
        ),
    )

    client = client_factory(responses)
    result = list(generate(client, parameters, progress))

    assert len(result) == 2


def test_generate_csv_rendered(progress, client_factory, response_factory, ff_request):
    responses = []

    parameters = {
        'date': {
            'after': '2021-12-01T00:00:00',
            'before': '2021-12-20T00:00:00',
        },
        'product': {
            'all': False,
            'choices': ['PRD-111-222-333'],
        },
        'mkp': {
            'all': False,
            'choices': ['MP-123'],
        },
    }

    responses.append(
        response_factory(
            query='ge(events.created.at,2021-12-01T00:00:00),le(events.created.at,2021-12-20T00:00:00),'
                  'eq(status,approved),eq(asset.params.id,nce_promo_final),in(asset.product.id,(PRD-111-222-333)),'
                  'in(marketplace.id,(MP-123))',
            value=ff_request,
        ),
    )
    client = client_factory(responses)
    result = list(generate(client, parameters, progress, renderer_type='csv'))

    assert len(result) == 3
    assert result[0] == HEADERS


def test_generate_json_render(progress, client_factory, response_factory, ff_request):
    responses = []

    parameters = {
        'date': {
            'after': '2021-12-01T00:00:00',
            'before': '2021-12-20T00:00:00',
        },
        'product': {
            'all': False,
            'choices': ['PRD-111-222-333'],
        },
    }

    responses.append(
        response_factory(
            query='ge(events.created.at,2021-12-01T00:00:00),le(events.created.at,2021-12-20T00:00:00),'
                  'eq(status,approved),eq(asset.params.id,nce_promo_final),in(asset.product.id,(PRD-111-222-333))',
            value=ff_request,
        ),
    )
    client = client_factory(responses)
    result = list(generate(client, parameters, progress, renderer_type='json'))

    assert len(result) == 2
    assert result[0]['request_id'] == 'PR-2'