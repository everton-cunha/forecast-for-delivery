import os
import numpy as np
import pandas as pd
import statistics

from datetime import datetime, timedelta


def forecasting(df):
    #pega as inforações de done e escopo
    done_list = df['done'].tolist()
    date_list = df['date'].tolist()
    total_list = df['total'].tolist()
    _execution = []
    #verifica se existe algo já feito para continuar
    if set(done_list) == {0}:
        return

    _execution = [done_list[i] - done_list[i-1]
                  for i in range(1, len(done_list))]
    _execution.append(done_list[0])
    if len(_execution) == 0:
        return
    _pencentil50 = np.percentile(_execution, 50)
    _pencentil75 = np.percentile(_execution, 75)

    execution = list(set(filter(lambda a: a != 0, _execution)))
    execution.sort()

    if len(execution) == 0:
        return

    df_best = pd.DataFrame({'date': [date_list[-1]], 'best': [done_list[-1]]})
    df_worst = pd.DataFrame(
        {'date': [date_list[-1]], 'worst': [done_list[-1]]})
    df_percentile_seventy_five = pd.DataFrame(
        {'date': [date_list[-1]], 'seventy_five': [done_list[-1]]})
    df_percentile_fifty = pd.DataFrame(
        {'date': [date_list[-1]], 'fifty': [done_list[-1]]})

    #monta a lista com o melhor caso
    _best = done_list[-1]
    _best_list = []
    while _best < total_list[-1]:
        _best += execution[-1]
        if _best <= total_list[-1]:
            _best_list.append(_best)
        else:
            if _best_list:
                _best_list.append(
                    _best_list[-1]+(total_list[-1] - _best_list[-1]))
            else:
                _best_list.append(_best+(total_list[-1] - _best))

    #monta a lista com o pior caso
    _worst = done_list[-1]
    _worst_list = []
    while _worst < total_list[-1]:
        _worst += execution[0]
        if _worst <= total_list[-1]:
            _worst_list.append(_worst)
        else:
            if _worst_list:
                _worst_list.append(
                    _worst_list[-1]+(total_list[-1] - _worst_list[-1]))
            else:
                _worst_list.append(_worst+(total_list[-1] - _worst))

    #monta a lista com o percentil75
    _percentile_seventy_five = done_list[-1]
    _percentile_seventy_five_list = []
    while _percentile_seventy_five < total_list[-1]:
        _percentile_seventy_five += _pencentil75
        if _percentile_seventy_five <= total_list[-1]:
            _percentile_seventy_five_list.append(_percentile_seventy_five)
        else:
            if _percentile_seventy_five_list:
                _percentile_seventy_five_list.append(
                    _percentile_seventy_five_list[-1]+(total_list[-1] - _percentile_seventy_five_list[-1]))
            else:
                _percentile_seventy_five_list.append(
                    _percentile_seventy_five+(total_list[-1] - _percentile_seventy_five))
    
    #monta a lista com o percentil50
    _percentile_fifty = done_list[-1]
    _percentile_fifty_list = []
    while _percentile_fifty < total_list[-1]:
        _percentile_fifty += _pencentil50
        if _percentile_fifty <= total_list[-1]:
            _percentile_fifty_list.append(_percentile_fifty)
        else:
            if _percentile_fifty_list:
                _percentile_fifty_list.append(
                    _percentile_fifty_list[-1]+(total_list[-1] - _percentile_fifty_list[-1]))
            else:
                _percentile_fifty_list.append(
                    _percentile_fifty+(total_list[-1] - _percentile_fifty))

    #identifica o ciclo que acontecem as entregas
    _cycle_delta = datetime.strptime(date_list[1], '%d/%m/%Y') - datetime.strptime(date_list[0], '%d/%m/%Y')
    datetime_object = datetime.strptime(date_list[-1], '%d/%m/%Y')
    _datetime_object = datetime_object
    for b in _best_list:
        _datetime_object = _datetime_object + timedelta(days=_cycle_delta.days)
        df_best = df_best.append(pd.DataFrame(
            {"date": [_datetime_object.strftime("%d/%m/%Y")], "best": [b], }), ignore_index=True)

    _datetime_object = datetime_object

    for w in _worst_list:
        _datetime_object = _datetime_object + timedelta(days=_cycle_delta.days)
        df_worst = df_worst.append(pd.DataFrame(
            {"date": [_datetime_object.strftime("%d/%m/%Y")], "worst": [w], }), ignore_index=True)

    _datetime_object = datetime_object

    for p in _percentile_seventy_five_list:
        _datetime_object = _datetime_object + timedelta(days=_cycle_delta.days)
        df_percentile_seventy_five = df_percentile_seventy_five.append(pd.DataFrame(
            {"date": [_datetime_object.strftime("%d/%m/%Y")], "seventy_five": [p], }), ignore_index=True)
    
    _datetime_object = datetime_object

    for pf in _percentile_fifty_list:
        _datetime_object = _datetime_object + timedelta(days=_cycle_delta.days)
        df_percentile_fifty = df_percentile_fifty.append(pd.DataFrame(
            {"date": [_datetime_object.strftime("%d/%m/%Y")], "fifty": [pf], }), ignore_index=True)

    df_bw = pd.merge(df_worst, df_best, how='outer', on='date')
    df_p = pd.merge(df_bw, df_percentile_seventy_five, how='outer', on='date')
    df_pf = pd.merge(df_p, df_percentile_fifty, how='outer', on='date')
    df_final = pd.merge(df, df_pf, how='outer', on='date')
    df_final[['total']] = df_final[['total']].fillna(value=total_list[-1])

    return df_final
