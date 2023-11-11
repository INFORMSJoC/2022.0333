# coding:utf-8
# @Time : 2022/8/12 21:29
# @Author : 郑攀
# @File ： ComS算法.py
# @Software : PyCharm
import csv

import numpy as np
import copy
from itertools import combinations
from derivative import diff_fun

def findoptimal(x_initial, ind_al, theta):
    solve = x_initial
    value = object_func(x_initial)
    one_index = list(np.where(np.array(x_initial) == 1)[0])

    x_combination = list(combinations(one_index, theta))
    ind_al_combination = list(combinations(ind_al, theta))
    # print(len(list(set(x_combination+ind_al_combination))))
    for x_sub in x_combination:
        x_initial_copy = copy.deepcopy(x_initial)
        for ind in x_sub:
            x_initial_copy[ind] = 0
        for ind_al_sub in ind_al_combination:
            if max([x_initial_copy[m] for m in ind_al_sub]) == 0:
                # print(i,j,value)
                for j in ind_al_sub:
                    x_initial_copy[j] = 1
                if object_func(x_initial_copy) < value:
                    solve = copy.deepcopy(x_initial_copy)
                    value = object_func(solve)
                for j in ind_al_sub:
                    x_initial_copy[j] = 0
    return solve

def greed(x_initial):
    x_one_index = list(np.where(np.array(x_initial) == 1)[0])
    value = 0
    solve = [0] * len(x_initial)
    for p in range(number_k):
        x_initial = copy.deepcopy(solve)
        for i in x_one_index:
            if x_initial[i] == 0:
                x_initial[i] = 1
                if object_func(x_initial) < value:
                    solve = copy.deepcopy(x_initial)
                    value = object_func(x_initial)
                x_initial[i] = 0
    return solve

import csv
import random
# import sympy as sp
# 函数表达式fun
from matplotlib import pyplot as plt


def twoloop(s, y, rho, gk):
    n = len(s)  # 向量序列的长度

    if np.shape(s)[0] >= 1:
        # h0是标量，而非矩阵
        h0 = 1.0 * np.dot(s[-1], y[-1]) / np.dot(y[-1], y[-1])
    else:
        h0 = 1

    a = np.empty((n,))

    q = gk.copy()
    for i in range(n - 1, -1, -1):
        a[i] = rho[i] * np.dot(s[i], q)
        q -= a[i] * y[i]
    z = h0 * q

    for i in range(n):
        b = rho[i] * np.dot(y[i], z)
        z += s[i] * (a[i] - b)

    return z


def lbfgs(fun, gfun, x0, m=5):
    # fun和gfun分别是目标函数及其一阶导数,x0是初值,m为储存的序列的大小
    maxk = 1
    rou = 0.55
    sigma = 0.4
    epsilon = 1e-5
    k = 0
    n = np.shape(x0)[0]  # 自变量的维度

    s, y, rho = [], [], []

    while k < maxk:
        gk = gfun(x0)
        if np.linalg.norm(gk) < epsilon:
            break

        dk = -1.0 * twoloop(s, y, rho, gk)

        m0 = 0
        mk = 0
        while m0 < 20:  # 用Armijo搜索求步长
            if fun(x0 + rou ** m0 * dk) < fun(x0) + sigma * rou ** m0 * np.dot(gk, dk):
                mk = m0
                break
            m0 += 1

        x = x0 + rou ** mk * dk
        sk = x - x0
        yk = gfun(x) - gk

        if np.dot(sk, yk) > 0:  # 增加新的向量
            rho.append(1.0 / np.dot(sk, yk))
            s.append(sk)
            y.append(yk)
        if np.shape(rho)[0] > m:  # 弃掉最旧向量
            rho.pop(0)
            s.pop(0)
            y.pop(0)

        k += 1
        x0 = x
        # print(fun(x0), k)
    return x0, fun(x0), k  # 分别是最优点坐标，最优值，迭代次数


features_set = ['repair_round', 'signal_strength', 'price_difference', 'box_seal', 'type_thing', 'price_update', 'camera_option', 'battery_rating', 'screen_line', 'card_issue', 'brand_delivery', 'design_flaw', 'camera_cover', 'battery_life', 'review_thing', 'customer_support', 'factory_reset', 'web_browser', 'verizon_app', 'use_lag', 'sim_smartphone', 'condition_deal', 'screen_response', 'seller_iphone', 'price_iphone', 'quality_product', 'battery_case', 'boot_loop', 'screen_look', 'pixel_life', 'network_setting', 'fingerprint_feature', 'software_support', 'side_edge', 'screen_problem', 'notification_light', 'app_transfer', 'water_damage', 'budget_phone', 'screen_feature', 'brand_one', 'google_service', 'condition_everything', 'paper_box', 'card_tool', 'quality_holder', 'work_great', 'speaker_output', 'call_quality', 'charger_money', 'side_effect', 'budget_upgrade', 'mode_etc', 'quality_body', 'touch_button', 'camera_feature', 'bar_none', 'processing_speed', 'screen_cell', 'scratch_right', 'price_everything', 'use_size', 'screen_speaker', 'camera_photo', 'type_cord', 'face_screen', 'brand_condition', 'charge_use', 'port_stopped', 'money_buy', 'factory_app', 'fingerprint_camera', 'battery_charger', 'battery_work', 'screen_half', 'camera_button', 'screen_glue', 'device_overall', 'software_hardware', 'display_issue', 'keyboard_thing', 'quality_item', 'voice_call', 'charger_right', 'life_product', 'processing_chip', 'zoom_len', 'sim_fit', 'quality_material', 'service_team', 'warranty_tech', 'screen_experience', 'brand_right', 'google_photo', 'top_scratch', 'camera_dot', 'speaker_sound', 'quality_hardware', 'card_tray', 'life_thing', 'sim_upgrade', 'home_charger', 'price_tag', 'camera_review', 'selfie_stick', 'touch_screen', 'budget_buy', 'price_pretty', 'color_display', 'boot_screen', 'app_work', 'image_quality', 'pixel_software', 'battery_fool', 'security_app', 'customer_experience', 'camera_performance', 'quality_control', 'pixel_release', 'camera_device', 'charge_cord', 'protector_condition', 'app_load', 'recognition_work', 'app_account', 'card_sound', 'back_damage', 'charger_nothing', 'android_software', 'hand_size', 'camera_glas', 'use_offer', 'back_scuff', 'repair_proces', 'scratch_protector', 'pixel_feature', 'price_seller', 'screen_picture', 'box_iphone', 'media_device', 'talk_customer', 'camera_camera', 'brand_seller', 'response_lack', 'garbage_piece', 'look_brand', 'cell_value', 'call_card', 'money_deal', 'battery_fan', 'battery_condition', 'seller_model', 'battery_design', 'port_issue', 'use_performance', 'cell_provider', 'edge_scratch', 'brand_new', 'design_overall', 'screen_view', 'cost_buy', 'card_deal', 'app_store', 'email_account', 'cell_battery', 'speaker_problem', 'camera_screen', 'connection_point', 'screen_ad', 'video_camera', 'review_bit', 'price_cost', 'battery_charge', 'line_top', 'look_condition', 'setting_set', 'quality_testing', 'side_button', 'use_mom', 'screen_cover', 'screen_chip', 'screen_big', 'screen_side', 'work_look', 'android_app', 'battery_use', 'body_cover', 'software_bloat', 'size_card', 'volume_control', 'screen_smartphone', 'screen_failure', 'price_screen', 'garbage_software', 'life_span', 'store_guy', 'service_provider', 'price_beat', 'screen_notification', 'charger_item', 'device_setting', 'port_mark', 'operating_system', 'app_format', 'corner_control', 'service_rep', 'display_refresh', 'screen_app', 'line_issue', 'money_pretty', 'battery_user', 'cell_quality', 'inch_right', 'case_backing', 'android_form', 'device_user', 'screen_gap', 'volume_issue', 'color_hue', 'price_item', 'price_phone', 'usage_month', 'brand_problem', 'cell_holder', 'brand_crack', 'quality_value', 'device_deal', 'store_price', 'cost_quality', 'use_month', 'video_file', 'camera_quality', 'memory_price', 'security_feature', 'point_year', 'cell_plan', 'price_spec', 'sim_problem', 'box_cover', 'mode_job', 'card_card', 'google_purchase', 'screen_button', 'home_use', 'brand_looking', 'call_sound', 'range_processor', 'signal_way', 'call_camera', 'price_drop', 'memory_capacity', 'internet_deal', 'screen_portion', 'pocket_fit', 'box_box', 'work_brand', 'device_feature', 'work_everything', 'life_user', 'setting_screen', 'money_lot', 'screen_quality', 'back_sensor', 'price_service', 'quality_video', 'selfie_cam', 'network_connection', 'screen_life', 'screen_tint', 'memory_card', 'case_choice', 'battery_problem', 'pixel_value', 'screen_gesture', 'edge_residue', 'shape_option', 'android_pie', 'sim_tool', 'display_quality', 'charger_unit', 'life_work', 'screen_area', 'paper_value', 'app_loading', 'note_charge', 'service_experience', 'home_screen', 'android_product', 'software_flaw', 'price_upgrade', 'work_fine', 'customer_service', 'wifi_calling', 'sound_quality', 'money_device', 'brand_nothing', 'speaker_hole', 'cell_happy', 'fingerprint_placement', 'pixel_bud', 'screen_bottom', 'money_value', 'wifi_connection', 'finger_reader', 'pixel_hope', 'app_amount', 'price_performance', 'home_button', 'app_user', 'note_camera', 'edge_replacement', 'case_lack', 'scratch_bit', 'voice_rate', 'service_connection', 'screen_pixel', 'work_price', 'cable_charger', 'quality_excellent', 'signal_area', 'camera_clarity', 'metal_body', 'app_space', 'boot_mode', 'fingerprint_no', 'screen_impact', 'port_plug', 'use_feature', 'screen_time', 'setting_change', 'charger_but', 'box_case', 'screen_break', 'sim_card', 'sim_attempt', 'screen_ton', 'screen_light', 'screen_gouge', 'camera_angle', 'seller_deal', 'quality_shipping', 'budget_product', 'back_camera', 'light_pic', 'face_work', 'work_problem', 'notch_cellphone', 'case_device', 'camera_experience', 'app_issue', 'quality_iphone', 'cost_provider', 'work_seller', 'sensor_spot', 'brand_speaker', 'google_ad', 'sim_speaker', 'talk_sim', 'screen_video', 'battery_power', 'google_functionality', 'performance_upgrade', 'life_factor', 'security_smartphone', 'performance_issue', 'rubber_web', 'angle_len', 'light_room', 'brand_experience', 'pixel_purchase', 'brand_battery', 'fingerprint_work', 'screen_work', 'protection_cover', 'screen_function', 'top_pixel', 'warranty_service', 'warranty_experience', 'price_battery', 'body_damage', 'charger_plug', 'device_price', 'wifi_signal', 'quality_sound', 'brand_time', 'condition_work', 'color_bit', 'battery_usage', 'battery_scratch', 'light_photo', 'company_line', 'call_volume', 'screen_iphone', 'use_ease', 'device_storage', 'price_condition', 'volume_setting', 'version_knock', 'use_product', 'price_way', 'ear_bud', 'face_unlock', 'android_version', 'camera_sound', 'review_issue', 'size_storage', 'battery_cover', 'bluetooth_connection', 'card_kit', 'voice_assistant', 'case_life', 'price_bargain', 'flagship_manufacturer', 'app_switching', 'use_limit', 'screen_bag', 'plastic_protector', 'budget_android', 'work_month', 'screen_condition', 'finger_scanner', 'device_scratch', 'screen_recording', 'screen_left', 'cell_user', 'app_bar', 'battery_seam', 'inch_size', 'fingerprint_unlock', 'quality_price', 'device_service', 'google_user', 'price_deal', 'quality_speaker', 'sprint_app', 'verizon_card', 'edge_time', 'voice_ability', 'photo_option', 'brand_life', 'condition_value', 'price_product', 'service_transfer', 'charge_adapter', 'condition_phone', 'performance_life', 'back_reader', 'price_option', 'headphone_pair', 'video_recording', 'connection_problem', 'price_buy', 'box_only', 'factory_film', 'home_key', 'money_wast', 'night_quality', 'card_capability', 'brand_item', 'mode_picture', 'call_button', 'cell_photo', 'health_app', 'budget_flagship', 'use_day', 'color_screen', 'face_feature', 'button_feature', 'seller_listing', 'display_display', 'price_unit', 'screen_protection', 'device_need', 'service_phone', 'battery_capacity', 'customer_care', 'display_screen', 'device_support', 'price_purchase', 'scratch_hole', 'android_phone', 'scratch_sign', 'app_icon', 'design_quality', 'app_feature', 'notch_screen', 'look_dark', 'seller_buying', 'carrier_voicemail', 'web_review', 'back_scratch', 'carrier_work', 'battery_amount', 'money_cell', 'sim_slot', 'edge_feature', 'security_concern', 'storage_brand', 'app_support', 'call_bar', 'display_price', 'box_cable', 'volume_problem', 'side_swipe', 'screen_size', 'factory_charger', 'case_smudge', 'condition_seller', 'power_use', 'size_option', 'plastic_material', 'memory_storage', 'google_google', 'cell_service', 'button_right', 'condition_product', 'software_issue', 'service_response', 'talk_service', 'money_junk', 'battery_indicator', 'pixel_camera', 'case_max', 'range_product', 'screen_cost', 'hand_fit', 'sprint_network', 'video_game', 'work_time', 'seller_product', 'inch_display', 'display_edge', 'brand_packaging', 'camera_money', 'camera_update', 'back_yard', 'recognition_software', 'back_blemish', 'picture_camera', 'fingerprint_option', 'card_work', 'touch_problem', 'app_corner', 'charger_port', 'warranty_cover', 'power_device', 'price_point', 'screen_imperfection', 'print_reader', 'camera_len', 'note_upgrade', 'point_phone', 'card_space', 'sim_swap', 'charge_plug', 'storage_space', 'flagship_model', 'card_capacity', 'size_screen', 'repair_shop', 'brand_issue', 'battery_phone', 'storage_screen', 'flagship_device', 'brand_price', 'back_crack', 'brand_unlocked', 'life_luck', 'sim_thing', 'camera_scratch', 'design_camera', 'setup_battery', 'sim_option', 'color_plug', 'money_screen', 'pixel_quality', 'charge_life', 'sim_port', 'battery_charging', 'print_scanner', 'camera_scanner', 'pixel_experience', 'picture_focu', 'seller_review', 'sim_phone', 'money_work', 'type_plug', 'card_slot', 'edge_screen', 'cell_work', 'sim_function', 'price_software', 'life_drain', 'software_iphone', 'network_connectivity', 'plastic_cover', 'money_feature', 'case_option', 'selfie_camera', 'customer_response', 'condition_iphone', 'battery_size', 'fingerprint_magnet', 'pocket_computer', 'pixel_way', 'device_speaker', 'service_call', 'display_glitch', 'bluetooth_issue', 'video_recorder', 'condition_lot', 'box_condition', 'camera_system', 'card_brand', 'screen_display', 'quality_device', 'device_fan', 'web_site', 'sim_version', 'customer_review', 'brand_cost', 'use_android', 'screen_ratio', 'line_addition', 'life_condition', 'camera_focu', 'finger_way', 'price_value', 'camera_price', 'volume_key', 'android_experience', 'pixel_user', 'device_problem', 'call_ringer', 'charge_day', 'plastic_case', 'display_feature', 'battery_draw', 'camera_setup', 'back_screen', 'price_state', 'screen_glas', 'price_enough', 'pixel_service', 'mode_switch', 'case_bar', 'flagship_value', 'screen_image', 'quality_delivery', 'night_photo', 'touch_sensitivity', 'quality_camera', 'device_day', 'voice_mail', 'use_iphone', 'budget_price', 'brand_product', 'water_skin', 'cell_signal', 'reader_trouble', 'screen_mark', 'corner_dent', 'brand_name', 'battery_drain', 'quality_processor', 'edge_performance', 'side_scratch', 'camera_expectation', 'corner_blemish', 'budget_device', 'memory_camera', 'work_day', 'brand_other', 'price_overall', 'device_app', 'brand_day', 'picture_opinion', 'picture_show', 'photo_editing', 'point_value', 'screen_saver', 'side_mark', 'card_upgrade', 'reader_no', 'brand_love', 'repair_service', 'customer_rep', 'speaker_work', 'photo_storage', 'power_cord', 'money_waste', 'use_time', 'angle_shot', 'card_reader', 'stereo_speaker', 'device_time', 'volume_button', 'quality_battery', 'speaker_issue', 'scratch_life', 'call_speaker', 'service_month', 'reader_thing', 'quality_audio', 'screen_sensitivity', 'wear_condition', 'condition_condition', 'response_time', 'sprint_call', 'night_shot', 'verizon_store', 'device_capability', 'version_cost', 'pixel_protector', 'screen_shield', 'pixel_ever', 'brand_brand', 'screen_corner', 'speaker_music', 'button_thing', 'device_use', 'battery_issue', 'camera_life', 'ear_port', 'carrier_device', 'app_bunch', 'screen_color', 'note_pro', 'card_swap', 'battery_function', 'port_damage', 'repair_option', 'talk_card', 'box_item', 'quality_picture', 'quality_life', 'work_product', 'price_feature', 'edge_plu', 'edge_upgrade', 'device_work', 'quality_difference', 'internet_service', 'screen_spot', 'power_switch', 'hand_experience', 'life_time', 'face_camera', 'wifi_feature', 'screen_aspect', 'edge_spot', 'protector_return', 'life_everything', 'screen_graphic', 'notification_setting', 'screen_type', 'camera_phone', 'brand_purchase', 'battery_percent', 'camera_crack', 'network_work', 'battery_value', 'battery_everything', 'condition_camera', 'software_performance', 'brand_seal', 'android_display', 'brand_device', 'mode_photo', 'power_button', 'web_use', 'app_lag', 'corner_crack', 'pixel_upgrade', 'type_cable', 'app_page', 'hand_touch', 'android_fan', 'cost_feature', 'edge_display', 'connection_issue', 'performance_way', 'video_call', 'back_case', 'speaker_audio', 'camera_area', 'google_storage', 'brand_top', 'box_store', 'network_issue', 'device_size', 'touch_issue', 'quality_screen', 'price_capacity', 'resolution_everything', 'processing_power', 'condition_came', 'size_phone', 'wear_sign', 'quality_feature', 'quality_issue', 'service_year', 'talk_text', 'android_system', 'reader_placement', 'price_love', 'print_sensor', 'price_android', 'ear_pod', 'camera_app', 'camera_capability', 'brand_scratch', 'notification_sound', 'battery_pack', 'finger_print', 'seller_job', 'color_love', 'sprint_work', 'verizon_work', 'seller_charger', 'case_glas', 'hand_market', 'battery_durability', 'factory_problem', 'corner_scratch', 'cell_camera', 'protector_bag', 'software_update', 'cell_carrier', 'picture_dark', 'screen_way', 'seller_service', 'work_picture', 'sim_holder', 'performance_ratio', 'photo_integration', 'brand_quality', 'work_thank', 'screen_scratch', 'display_scratch', 'screen_part', 'price_experience', 'use_phone', 'money_purchase', 'price_replacement', 'screen_screen', 'pixel_transfer', 'app_option', 'signal_reception', 'warranty_lemon', 'device_protection', 'app_version', 'display_size', 'price_feel', 'brand_phone', 'email_use', 'condition_corner', 'brand_charger', 'performance_mode', 'money_option', 'quality_everything', 'quality_check', 'touch_operation', 'service_product', 'cell_seller', 'app_developer', 'fingerprint_button', 'use_sign', 'sound_glitch', 'customer_time', 'hand_side', 'review_date', 'use_week', 'camera_smart', 'factory_thing', 'pixel_condition', 'side_crack', 'paper_clip', 'camera_lens', 'hand_feature', 'price_lot', 'hand_speaker', 'android_way', 'android_thing', 'service_time', 'shape_life', 'call_connectivity', 'box_right', 'power_iphone', 'photo_capability', 'company_service', 'pixel_version', 'work_email', 'usage_part', 'camera_function', 'side_issue', 'box_scratch', 'back_button', 'screen_crack', 'card_phone', 'light_performance', 'case_fit', 'camera_processor', 'call_reception', 'money_quality', 'size_camera', 'display_brightnes', 'screen_element', 'back_gouge', 'pixel_update', 'case_variety', 'range_spec', 'cell_connection', 'condition_nothing', 'display_color', 'system_spec', 'voice_recognition', 'corner_pixel', 'card_speaker', 'screen_blob', 'performance_smartphone', 'brand_protector', 'device_weight', 'memory_option', 'screen_issue', 'quality_wen', 'scratch_mark', 'screen_repair', 'software_upgrade', 'case_scenario', 'note_screen', 'scratch_screen', 'window_phone', 'light_shot', 'talk_time', 'camera_user', 'screen_malfunction', 'recognition_lock', 'fingerprint_recognition', 'edge_spec', 'power_management', 'cell_condition', 'screen_battery', 'recognition_ability', 'call_use', 'health_condition', 'charger_packaging', 'edge_touch', 'finger_recognition', 'quality_phone', 'fingerprint_reader', 'protection_case', 'camera_shot', 'factory_condition', 'battery_defect', 'light_filter', 'cable_support', 'edge_glas', 'app_use', 'charger_condition', 'volume_speaker', 'cost_replacement', 'back_cover', 'screen_replacement', 'screen_clarity', 'display_view', 'cable_adapter', 'camera_damage', 'processor_game', 'pixel_bar', 'camera_processing', 'use_year', 'quality_glas', 'sim_provider', 'display_corner', 'camera_value', 'app_button', 'price_job', 'back_nick', 'cost_phone', 'version_price', 'volume_level', 'system_update', 'software_glitch', 'work_phone', 'budget_tier', 'store_charge', 'face_right', 'top_speaker', 'price_choice', 'use_hour', 'angle_cam', 'screen_touch', 'battery_performance', 'price_cell', 'app_acces', 'fingerprint_sensor', 'camera_resolution', 'recognition_app', 'app_list', 'color_image', 'version_plan', 'box_envelope', 'side_line', 'video_app', 'charger_cord', 'device_issue', 'light_leak', 'camera_picture', 'price_thing', 'photo_space', 'sim_number', 'carrier_store', 'screen_edge', 'charge_cycle', 'media_app', 'carrier_version', 'app_storage', 'pixel_performance', 'device_function', 'sim_support', 'app_number', 'screen_operation', 'scratch_condition', 'paper_weight', 'night_picture', 'network_type', 'quality_smartphone', 'quality_capture', 'side_condition', 'carrier_feature', 'top_top', 'storage_lot', 'screen_performance', 'work_issue', 'power_thing', 'screen_hole', 'camera_ram', 'window_app', 'network_buy', 'seller_purchase', 'size_life', 'cell_company', 'cell_pricing', 'app_mix', 'hand_product', 'inch_screen', 'life_purchase', 'rubber_case', 'light_picture', 'card_feature', 'camera_issue', 'budget_option', 'touch_keyboard', 'type_stuff', 'speaker_etc', 'top_skin', 'screen_tap', 'price_side', 'pixel_screen', 'color_look', 'pixel_return', 'use_life', 'screen_scuff', 'brand_feature', 'quality_storage', 'android_user', 'smart_option', 'camera_difference', 'photo_camera', 'google_tech', 'life_life', 'setting_feature', 'screen_thing', 'android_update', 'app_crash', 'case_protector', 'android_exp', 'headphone_quality', 'android_day', 'quality_display', 'camera_notch', 'audio_bit', 'edge_corner', 'print_way', 'company_work', 'color_option', 'google_series', 'network_problem', 'quality_adapter', 'brand_screen', 'screen_right', 'sim_sim', 'headphone_cable', 'app_app', 'sim_feature', 'color_pink', 'brand_shape', 'point_device', 'battery_percentage', 'cost_product', 'corner_scuff', 'wear_mark', 'photo_quality', 'design_choice', 'range_camera', 'pixel_issue', 'brand_model', 'pixel_info', 'service_card', 'charge_damage', 'cell_phone', 'speaker_volume', 'seller_experience', 'price_issue', 'service_work', 'pixel_photography', 'device_condition', 'pixel_google', 'top_bar', 'use_spec', 'review_part', 'scratch_shape', 'box_number', 'money_product', 'money_phone', 'money_amount', 'warranty_not', 'charger_charge', 'top_feature', 'face_reader', 'price_speed', 'box_brand', 'verizon_system', 'box_charger', 'charge_time', 'quality_case', 'quality_problem', 'face_recognition', 'web_load', 'sim_service', 'network_carrier', 'side_way', 'speaker_scratch', 'camera_hardware', 'app_room', 'android_feature', 'brand_thing', 'camera_work', 'ear_speaker', 'app_memory', 'software_problem', 'brand_case', 'back_fingerprint', 'touch_option', 'work_love', 'edge_button', 'cell_reception', 'brand_iphone', 'carrier_plan', 'case_work', 'type_charger', 'quality_photo', 'power_port', 'warranty_month', 'carrier_card', 'work_value', 'headphone_jack', 'look_new', 'call_problem', 'angle_camera', 'device_experience', 'charger_air', 'color_experience', 'company_product', 'picture_quality', 'point_picture', 'condition_shipping', 'touch_way', 'device_review', 'color_balance', 'app_setting', 'battery_health', 'use_card', 'color_quality', 'carrier_issue', 'touch_design', 'carrier_switch', 'charge_port', 'photo_backup', 'price_range', 'service_representative', 'condition_range', 'brand_buy', 'screen_brightnes', 'sim_reader', 'recognition_feature', 'size_font', 'touch_control', 'inch_scratch', 'box_accessory', 'sprint_store', 'card_storage', 'audio_play', 'video_capture', 'box_app', 'touch_feature', 'app_task', 'screen_space', 'camera_thing', 'device_thing', 'size_speaker', 'screen_protector', 'edge_look', 'sim_tray', 'camera_software', 'performance_value', 'brand_deal', 'battery_hour', 'use_case', 'line_person', 'battery_day', 'storage_feature', 'screen_spec', 'speaker_something', 'screen_setup', 'smart_phone', 'screen_damage', 'battery_camera', 'quality_charger', 'brand_everything', 'screen_viewing', 'battery_product', 'app_performance', 'screen_device', 'screen_glitch', 'review_option', 'night_mode', 'touch_response', 'customer_direct', 'call_gaming', 'metal_case', 'performance_improvement', 'display_reading', 'work_health', 'android_support', 'battery_time', 'shape_everything']

pro_features_1 = []
importance_performance_1 = []
with open('Data/B08BGD4G36.csv', "r", encoding='utf8') as f:  # 打开文件
    lines = csv.reader(f)
    for line in lines:
        importance_performance_1.append([50 * float(line[1]), float(line[2])])
        pro_features_1.append(line[0])

pro_features_2 = []
importance_performance_2 = []
with open('Data/B08BJJ1T9F.csv', "r", encoding='utf8') as f:  # 打开文件
    lines = csv.reader(f)
    for line in lines:
        importance_performance_2.append([50 * float(line[1]), float(line[2])])
        pro_features_2.append(line[0])

features_no_repeat_dic = {}
pro_features = pro_features_1 + pro_features_2
pro_features_set = list(set(pro_features))
for i in range(len(pro_features_set)):
    features_no_repeat_dic[pro_features_set[i]] = i

competitiveness_inverse = []
with open('Data/Com_network_10.csv', "r", encoding='utf8') as f:  # 打开文件
    lines = csv.reader(f)
    for line in lines:
        competitiveness_inverse.append([float(m) for m in line])


competitiveness_dic = {}
for i in range(len(competitiveness_inverse[0])):
    competitiveness_dic[features_set[i]] = [competitiveness_inverse[j][i] for j in range(len(competitiveness_inverse))]

# print(feature_matrix[0])

def object_func(x):
    object = 0
    for i in range(len(x)):
        object = object + x[i] * (feature_matrix[i][0] + feature_matrix[i][1])

    for i in range(len(feature_matrix[0]) - 2):
        com_set = []
        com_x = []
        for j in range(len(x)):
            if feature_matrix[j][i + 2] != 1:
                com_set.append(x[j] * feature_matrix[j][i + 2])
                com_x.append(x[j])
                # print(feature_matrix[j][i + 2])

        if sum(com_x) != 0:
            object = object + sum(com_set) / (sum(com_x))
    return -object


gfun_list = diff_fun()
fun = lambda x: object_func(x)
# 梯度向量 gfun
def initialsolver(initial_solution, n):
    rt = lbfgs(fun, gfun_list[n], initial_solution)
    return rt[0]

number_k = 15
fp = open('Output/PI_gamma_k=15.csv', "w+", encoding='utf8', newline='')
write = csv.writer(fp)

for n in range(0,10):
    review_number = 40 * (n + 1)
    pi = [review_number]

    for gamma in range(0,21):
        l = 3
        print(n, gamma)
        lam = 0.05*l

        feature_matrix = []
        for i in range(len(pro_features_1)):
            feature_matrix.append(importance_performance_1[i] + competitiveness_dic[pro_features_1[i]])

        for i in range(len(pro_features_2)):
            feature_matrix.append(importance_performance_2[i] + competitiveness_dic[pro_features_2[i]])
        feature_matrix = feature_matrix[0:review_number]

        x_optimal = [0.6] * review_number
        x_initial = initialsolver(x_optimal, n)
        x_initial = list(x_initial)

        for i in range(max([number_k,int(len(x_initial)*lam)])):
            ind = x_initial.index(max(x_initial))
            x_initial[ind] = -1

        ind_al = []
        x_initial_al = copy.deepcopy(x_initial)
        for i in range(int(len(x_initial)*(1-lam)*gamma*0.05)):
            ind = x_initial_al.index(max(x_initial_al))
            ind_al.append(ind)
            x_initial_al[ind] = -1

        for i in range(len(x_initial)):
            if x_initial[i] == -1:
                x_initial[i] = 1
            else:
                x_initial[i] = 0

        gr = greed(x_initial)

        x_optimal = gr

        for p in [1]:
            while 1:
                x_last_in = object_func(x_optimal)
                x_optimal = findoptimal(x_optimal, ind_al, p)
                # print(review_number, lam, p, object_func(x_optimal), sum(x_optimal))
                if object_func(x_optimal) == x_last_in:
                    break

            # write.writerow([review_number, lam, p, object_func(x_optimal), sum(x_optimal)])
            pi.append(object_func(x_optimal))
    write.writerow(pi)
    print(pi)
