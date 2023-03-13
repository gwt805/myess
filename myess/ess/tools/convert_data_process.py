from ess import models
'''
标注数量
结算方式
单价
'''
def convert_data_process():
    alld = models.Waibao.objects.all()
    print(f'总共有 {len(alld)} 条数据')
    flag_list = []
    for i in alld:
        flag = models.Waibao.objects.filter(
            pname=i.pname, pnums=i.pnums, get_data_time=i.get_data_time)
        if len(flag) == 1:
            # 添加数据
            dataone = {
                'user': models.User.objects.get(username=models.User.objects.get(zh_uname='郭卫焘').username),
                'proname': models.Project.objects.get(pname=i.pname),
                'send_data_time': "2021-01-01",
                'pnums': i.pnums,
                'data_source': "未知",
                'scene': "未知",
                'send_reason': "未知",
                'key_frame_extracted_methods': "未知",
                'begin_check_data_time': "2021-01-01",
                'last_check_data_time': "2021-01-01",
                'get_data_time': i.get_data_time,
                'ann_meta_data': [{'recovery_precision': None, 'knums': i.knums, "settlement_method":i.settlement_method, "unit_price": round(i.unit_price,3)}],
                'wb_name': models.Waibaos.objects.get(name=i.wb_name),
                'created_time': "2021-01-01",
                'total_money': round(i.knums*i.unit_price,3)
            }
            models.Supplier.objects.create(**dataone)
            print("单条添加成功: ",i.pname, i.pnums,i.get_data_time,i.knums,i.settlement_method,round(i.unit_price,3),i.wb_name,round(i.knums*i.unit_price,3))
        else:
            pnums_list = []
            knums_list = []
            unit_price_list = []
            get_time_list = []
            settlement_method_list = []
            ann_meta_data = []
            total_money = 0
            for i in flag:
                if i.pnums not in pnums_list:
                    pnums_list.append(i.pnums)
                if i.get_data_time not in get_time_list:
                    get_time_list.append(i.get_data_time)
                knums_list.append(i.knums)
                unit_price_list.append(round(i.unit_price,2))
                settlement_method_list.append(i.settlement_method)
            

                total_money += (i.knums * i.unit_price)
            
            for item in zip(knums_list, settlement_method_list, unit_price_list):
                ann_meta_data.append({
                    'recovery_precision': None,
                    'knums': item[0],
                    "settlement_method": item[1],
                    "unit_price": round(item[2], 3)
                })
            
            if (get_time_list, pnums_list) not in flag_list:
                flag_list.append((get_time_list, pnums_list))
                # 添加数据
                datamanny = {
                    'user': models.User.objects.get(username=models.User.objects.get(zh_uname='郭卫焘').username),
                    'proname': models.Project.objects.get(pname=i.pname),
                    'send_data_time': "2021-01-01",
                    'pnums': pnums_list[0],
                    'data_source': "未知",
                    'scene': "未知",
                    'send_reason': "未知",
                    'key_frame_extracted_methods': "未知",
                    'begin_check_data_time': "2021-01-01",
                    'last_check_data_time': "2021-01-01",
                    'ann_meta_data': ann_meta_data,
                    'get_data_time': get_time_list[0],
                    'wb_name': models.Waibaos.objects.get(name=i.wb_name),
                    'created_time': "2021-01-01",
                    'total_money': round(total_money,3)
                }
                models.Supplier.objects.create(**datamanny)
                print("多条添加成功: ",i.pname, pnums_list,get_time_list,knums_list,settlement_method_list,unit_price_list,i.wb_name,round(total_money,3))
            else:
                print("已经添加过了")