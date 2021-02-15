import os
import numpy as np
import pandas as pd
import statistics

from datetime import datetime, timedelta

def _list_build(done_list, total_list, deliveries):
    _case = done_list[-1]
    _case_list = []
    while _case < total_list[-1]:
        _case += deliveries
        if _case <= total_list[-1]:
            _case_list.append(_case)
        else:
            if _case_list:
                _case_list.append(
                    _case_list[-1]+(total_list[-1] - _case_list[-1]))
            else:
                _case_list.append(_case+(total_list[-1] - _case))
    return _case_list



def forecasting(df):
    #pega as inforações de done e escopo
    done_list = df['done'].tolist()
    date_list = df['date'].tolist()
    total_list = df['total'].tolist()
    deliveries = []
    # deliveries
    #verifica se existe algo já feito para continuar
    if set(done_list) == {0}:
        return

    deliveries = [done_list[i] - done_list[i-1]
                  for i in range(1, len(done_list))]
    deliveries.append(done_list[0])
    if len(deliveries) == 0:
        return
    
    _pencentil50 = int(np.percentile(deliveries, 50))
    _pencentil75 = int(np.percentile(deliveries, 75))

    deliveries = list(set(filter(lambda a: a != 0, deliveries)))
    deliveries.sort()

    if len(deliveries) == 0:
        return

    df_best = pd.DataFrame({'date': [date_list[-1]], 'best': [done_list[-1]]})
    df_worst = pd.DataFrame(
        {'date': [date_list[-1]], 'worst': [done_list[-1]]})
    df_percentile_seventy_five = pd.DataFrame(
        {'date': [date_list[-1]], 'seventy_five': [done_list[-1]]})
    df_percentile_fifty = pd.DataFrame(
        {'date': [date_list[-1]], 'fifty': [done_list[-1]]})

    #monta a lista com o melhor caso
    _best_list = _list_build(done_list, total_list, deliveries[-1])

    #monta a lista com o pior caso
    _worst_list = _list_build(done_list, total_list, deliveries[0])

    #monta a lista com o percentil75
    _percentile_seventy_five_list = _list_build(done_list, total_list, _pencentil75)
    
    #monta a lista com o percentil50
    _percentile_fifty_list = _list_build(done_list, total_list, _pencentil50)

    #identifica o ciclo que acontecem as entregas
    if len(date_list) > 1:
        _cycle_delta = datetime.strptime(date_list[1], '%d/%m/%Y') - datetime.strptime(date_list[0], '%d/%m/%Y')
    else:
        _cycle_delta = datetime.strptime(date_list[0], '%d/%m/%Y')
    datetime_object = datetime.strptime(date_list[-1], '%d/%m/%Y')
    _datetime_object = datetime_object
    for b in _best_list:
        if len(date_list) > 1:
            _datetime_object = _datetime_object + timedelta(days=_cycle_delta.days)
        else:
            _datetime_object = _datetime_object + timedelta(days=7)
        df_best = df_best.append(pd.DataFrame(
            {"date": [_datetime_object.strftime("%d/%m/%Y")], "best": [b], }), ignore_index=True)

    _datetime_object = datetime_object

    for w in _worst_list:
        _datetime_object = _datetime_object + timedelta(days=7)
        df_worst = df_worst.append(pd.DataFrame(
            {"date": [_datetime_object.strftime("%d/%m/%Y")], "worst": [w], }), ignore_index=True)

    _datetime_object = datetime_object

    for p in _percentile_seventy_five_list:
        if len(date_list) > 1:
            _datetime_object = _datetime_object + timedelta(days=_cycle_delta.days)
        else:
            _datetime_object = _datetime_object + timedelta(days=7)
        df_percentile_seventy_five = df_percentile_seventy_five.append(pd.DataFrame(
            {"date": [_datetime_object.strftime("%d/%m/%Y")], "seventy_five": [p], }), ignore_index=True)
    
    _datetime_object = datetime_object

    for pf in _percentile_fifty_list:
        if len(date_list) > 1:
            _datetime_object = _datetime_object + timedelta(days=_cycle_delta.days)
        else:
            _datetime_object = _datetime_object + timedelta(days=7)
        df_percentile_fifty = df_percentile_fifty.append(pd.DataFrame(
            {"date": [_datetime_object.strftime("%d/%m/%Y")], "fifty": [pf], }), ignore_index=True)

    df_bw = pd.merge(df_worst, df_best, how='outer', on='date')
    df_p = pd.merge(df_bw, df_percentile_seventy_five, how='outer', on='date')
    df_pf = pd.merge(df_p, df_percentile_fifty, how='outer', on='date')
    df_final = pd.merge(df, df_pf, how='outer', on='date')
    df_final[['total']] = df_final[['total']].fillna(value=total_list[-1])

    return df_final
