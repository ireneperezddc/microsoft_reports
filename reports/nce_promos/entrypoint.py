# -*- coding: utf-8 -*-
#
# Copyright (c) 2021, Ingram Micro
# All rights reserved.

from reports.utils import get_basic_value, get_value, parameter_value, convert_to_datetime

HEADERS = (
    'Request Type', 'Request ID', 'Product ID', 'Product Name', 'Request Created At', 'Subscription Created At',
    'Subscription ID', 'Subscription Status', 'Subscription External ID', 'Promotion Applied (%)',
    'Microsoft Tenant ID', 'Microsoft Domain', 'Microsoft Subscription ID', 'Microsoft Order ID', 'Microsoft Plan ID',
    'Item ID', 'Item MPN', 'Item Name', 'Item Period', 'Item Quantity', 'Marketplace Name',
    'Microsoft Tier1 MPN (if any)', 'Customer ID'
)

TIER_CONFIGS = {}


def generate(
        client=None,
        parameters=None,
        progress_callback=None,
        renderer_type=None,
        extra_context_callback=None,
):
    requests = _get_request_list(client, parameters)

    progress = 0
    total = len(requests)
    if renderer_type == 'csv':
        yield HEADERS
        progress += 1
        total += 1
        progress_callback(progress, total)

    for request in requests:
        if renderer_type == 'json':
            yield {
                HEADERS[idx].replace(' ', '_').lower(): value
                for idx, value in enumerate(_process_line(client, request))
            }
        else:
            yield _process_line(client, request)
        progress += 1
        progress_callback(progress, total)


def _get_request_list(client, parameters):
    query = [
        f'ge(events.created.at,{parameters["date"]["after"]})',
        f'le(events.created.at,{parameters["date"]["before"]})',
        'eq(status,approved)',
        'eq(asset.params.id,nce_promo_final)'
    ]

    if parameters.get('product') and parameters['product']['all'] is False:
        query.append(f'in(asset.product.id,({",".join(parameters["product"]["choices"])}))')
    if parameters.get('mkp') and parameters['mkp']['all'] is False:
        query.append(f'in(marketplace.id,({",".join(parameters["mkp"]["choices"])}))')

    result = client.requests.filter(','.join(query))

    requests = []
    for request in result:
        if parameter_value('nce_promo_final', request['asset']['params']):
            requests.append(request)

    return requests


def _get_tier1_mpn(client, product_id, account_id):
    if product_id not in TIER_CONFIGS:
        TIER_CONFIGS[product_id] = {}

    if account_id not in TIER_CONFIGS[product_id]:
        TIER_CONFIGS[product_id][account_id] = "-"
        query = [
            f'eq(product.id,{product_id})',
            f'eq(account.id,{account_id})'
        ]
        result = client.ns('tier').collection('configs').filter(','.join(query))
        for config in result:
            TIER_CONFIGS[product_id][account_id] = parameter_value('tier1_mpn', config['params'])

    return TIER_CONFIGS[product_id][account_id]


def _process_line(client, request):
    promotion = parameter_value('nce_promo_final', request['asset']['params'])
    tier1_mpn = _get_tier1_mpn(
        client,
        get_value(request['asset'], 'product', 'id'),
        get_value(request['asset']['tiers'], 'tier1', 'id')
    )
    return (
        get_basic_value(request, 'type'),
        get_basic_value(request, 'id'),
        get_value(request['asset'], 'product', 'id'),
        get_value(request['asset'], 'product', 'name'),
        convert_to_datetime(get_basic_value(request, 'created')),
        convert_to_datetime(get_value(request['asset']['events'], 'created', 'at')),
        get_value(request, 'asset', 'id'),
        get_value(request, 'asset', 'status'),
        get_value(request, 'asset', 'external_id'),
        promotion['promotions'][0]['discount_percent'],
        parameter_value('ms_customer_id', request['asset']['params']),
        parameter_value('microsoft_domain', request['asset']['params']),
        parameter_value('subscription_id', request['asset']['params']),
        parameter_value('csp_order_id', request['asset']['params']),
        '-',
        get_basic_value(request['asset']['items'][0], 'id'),
        get_basic_value(request['asset']['items'][0], 'mpn'),
        get_basic_value(request['asset']['items'][0], 'display_name'),
        get_basic_value(request['asset']['items'][0], 'period'),
        get_basic_value(request['asset']['items'][0], 'quantity'),
        get_value(request['asset'], 'marketplace', 'name'),
        tier1_mpn,
        get_value(request['asset']['tiers'], 'customer', 'id')
    )
