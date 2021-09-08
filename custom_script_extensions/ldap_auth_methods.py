from ldap3 import Server, Connection, ALL, SUBTREE, LEVEL
import logging
import sys
import os

from django_python3_ldap.utils import sync_user_relations
from django_python3_ldap.utils import clean_user_data
from custom_script_extensions.djangoanalytics_initialize import get_or_create_groups, add_groups_to_users, update_user_groups, update_user_extra_data


logger = logging.getLogger(__name__)


def update_user_sadko_groups(user):
    from django.db import connections
    from django.contrib.auth.models import User, Group

    conn_sadko = connections['dash_sadko_postgres_db']
    if conn_sadko.connection is None:
        cursor = conn_sadko.cursor()  
    
    sql="""""""

    cursor = conn_sadko.connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchone()

    if results is not None:
        django_exists_sadko_roles = list(Group.objects.filter(name__startswith='SADKO_').values_list('name', flat=True))
        sadko_roles = []
        sadko_roles_user_text = []
        sadko_user_is_blocked = False

        for index, row in enumerate(cursor):
            if row[4] or row[5]: sadko_user_is_blocked = True
            if index > 200:
                break
            else:
                role = row[2]
                sadko_roles_user_text.append(role)
                if role not in django_exists_sadko_roles:
                    sadko_roles.append(Group(name=role))

        u = User.objects.get(username=user)
        g = Group.objects.filter(name__startswith='SADKO_').all()
        u.groups.remove(g)
        if sadko_user_is_blocked == False:
            if len(sadko_roles) > 0:
                Group.objects.bulk_create(sadko_roles)

            for r in sadko_roles_user_text:
                g = Group.objects.get(name=r)
                u.groups.add(g) 
            u.save()

    cursor.close()

# if user auth via LDAP - check status and update connection
# from custom_script_extensions.ldap_auth_methods import ldap_open_connetion, ldap_check_user_is_active, ldap_check_user_exists_in_group

# auth_ldap_user = 'username'
# user_requeired_ldap_groups = [
#     'group1',
#     'group2',
#     'group3'
# ]
# ldap_server = 'ldap_server'
# ldap_domain = 'domain'
# ldap_dc1 = 'domain_1'
# ldap_dc2 = 'domain_2'
# ldap_dc3 = 'domain_3'
# ldap_user = 'username'
# ldap_password = 'password'


# users = ['user1', 'user2', 'user3']
# users = ['user1']

# conn = ldap_open_connetion(ldap_server=ldap_server, ldap_domain=ldap_domain, ldap_user=ldap_user, ldap_password=ldap_password)
# for u in users:
#     auth_ldap_user = u
#     result = ldap_check_user_is_active(
#         conn=conn, 
#         ldap_user_login=auth_ldap_user, 
#         ldap_dc1=ldap_dc1, 
#         ldap_dc2=ldap_dc2, 
#         ldap_dc3=ldap_dc3)
#     #print('ldap_check_user_is_active:', 'auth_ldap_user', auth_ldap_user, 'result', result)
#     if result:
#         for group in user_requeired_ldap_groups:
#             result = ldap_check_user_exists_in_group(
#                 conn=conn, 
#                 ldap_user_login=auth_ldap_user, 
#                 ldap_search_group=group, 
#                 ldap_dc1=ldap_dc1, 
#                 ldap_dc2=ldap_dc2, 
#                 ldap_dc3=ldap_dc3)
#             #print('ldap_check_user_exists_in_group:', 'auth_ldap_user', auth_ldap_user, 'group', group, 'result', result)



def ldap_open_connetion(ldap_server, ldap_domain, ldap_user, ldap_password):
    server = Server(f'ldap://{ldap_server}', use_ssl=True, get_info=ALL)
    conn = Connection(server,
        check_names=False, 
        auto_bind=False,
        user=f"{ldap_domain}\\{ldap_user}",
        password=f"{ldap_password}", 
        authentication="NTLM")
    conn.open()
    return conn


def ldap_check_user_is_active(conn=None, ldap_user_login=None, ldap_dc1=None, ldap_dc2=None, ldap_dc3=None):
    status = False

    if type(conn).__name__ != 'Connection': 
        logger.error(f'ldap_check_user_is_active: connection fail {type(conn).__name__ }.')
        return status
    if ldap_user_login is None or ldap_dc1 is None or ldap_dc2 is None or ldap_dc3 is None: 
        logger.error(f'ldap_check_user_is_active: params fail.')
        return status 

    conn.bind()
    if conn.bind():
        conn.search(search_base=f'DC={ldap_dc1},DC={ldap_dc2},DC={ldap_dc3}', 
            search_filter=f'(&(objectClass=user)(sAMAccountName={ldap_user_login}))',
            search_scope=SUBTREE,
            attributes=['userAccountControl'])
        if len(conn.entries) > 0:
            results = conn.entries[0]
            
            for result in results:
                for i in result:
                    if i == '512':
                        status = True
                        break
        conn.unbind()
    logger.info(f'ldap_check_user_is_active: ldap_user_login {ldap_user_login}, result {status}')
    return status


def ldap_check_user_exists_in_group(conn=None, ldap_user_login=None, ldap_search_group=None, ldap_dc1=None, ldap_dc2=None, ldap_dc3=None):
    status = False

    if type(conn).__name__ != 'Connection': 
        logger.error(f'ldap_check_user_exists_in_group: connection fail {type(conn).__name__ }.')
        return status
    if ldap_user_login is None or ldap_search_group is None or ldap_dc1 is None or ldap_dc2 is None or ldap_dc3 is None: 
        logger.error(f'ldap_check_user_exists_in_group: params fail.')
        return status 

    conn.bind()
    if conn.bind():
        conn.search(search_base=f'DC={ldap_dc1},DC={ldap_dc2},DC={ldap_dc3}', 
            search_filter=f'(&(objectClass=GROUP)(CN={ldap_search_group}))',
            search_scope=SUBTREE,
            attributes=['member'])
        if len(conn.entries) > 0:
            results = conn.entries[0]
            
            for result in results:
                for i in result:
                    if ldap_user_login in i:
                        status = True
                        break
        conn.unbind()
        logger.info(f'ldap_check_user_exists_in_group: auth_ldap_user {ldap_user_login}, group {ldap_search_group}, result {status}')
    return status



# from ldap3 import Server, Connection, ALL, SUBTREE, LEVEL
# conn = Connection(Server(
#         config('LDAP_URL', default=''), 
#         #use_ssl=True,
#         get_info=ALL),
#     check_names=False, 
#     auto_bind=False,
#     user=f"{config('LDAP_DOMAIN', default='')}\\{config('LDAP_USERNAME', default='')}",
#     password=config('LDAP_PASSWORD', default=''), 
#     authentication="NTLM")
# conn = Connection(Server(
#         'ldap://server', 
#         #use_ssl=True,
#         get_info=ALL),
#     check_names=False, 
#     auto_bind=False,
#     user="domain\\login",
#     password="password", 
#     authentication="NTLM")
# conn.open()
# conn.bind()
# print(conn)
# print(conn.result)
# print(conn.extend.standard.who_am_i())
# if conn.bind():
    # conn.search('DC=domain-name-part-1,DC=domain-name-part-2,DC=domain-name-part-3', "(&(objectClass=user)(sAMAccountName=login_name))", 
    #     SUBTREE, 
    #     attributes=['sAMAccountName', 'displayName', 'userAccountControl', 'department', 'division', 'title', 'mail', 'sn', 'givenName', 'memberOF'])

    # # userAccountControl // 512 = NON-banned, 514 = banned
    # # attributes='*' // all columns
    # # conn.entries // all results
    # # print(conn.response_to_json()) // results to json 

    # for i in conn.entries:
    #     print('login_name:{0}, full_name:{1}, account_status:{2}, email:{3}, department:{4}, center:{5}, position:{6}, name:{7}, last_name:{8}, user_groups:{9}'.format(
    #         i.sAMAccountName.values[0], 
    #         i.displayName.values[0], 
    #         i.userAccountControl.values[0],
    #         i.department.values[0],
    #         i.division.values[0],
    #         i.title.values[0],
    #         i.mail.values[0],
    #         i.sn.values[0],
    #         i.givenName.values[0],
    #         i.memberOF.values[0]))
# conn.unbind()
# check if user exists in group




def custom_sync_user_relations(user, data):
    ldap_is_active = False
    if data.get('userAccountControl', None)[0] in ['512', '544', '66048', '66080']:
        ldap_is_active = True

    ldap_groups = list(data.get('memberOf', ()))
    clean_ldap_groups = []
    for group in ldap_groups:
        if '_Groups' in group:
            g = group[3:group.find(',')]
            g = 'LDAP_' + g
            clean_ldap_groups.append(g)
    get_or_create_groups(clean_ldap_groups, bulk_create=True)
    for item in clean_ldap_groups:
        add_groups_to_users(user, item)
    update_user_groups(user, clean_ldap_groups, 'LDAP')
    #update_user_sadko_groups(user)

    extra_data = [
        {'full_name': data.get('displayName', None)},
        {'department': data.get('department', None)},
        {'center': data.get('division', None)},
        {'position': data.get('title', None)},
        {'name': data.get('sn', None)},
        {'last_name': data.get('givenName', None)},
        {'ldap_is_active': ldap_is_active}
    ]
    update_user_extra_data(user, extra_data)
    #update_user_sadko_groups(user)
    
    return user, data


def custom_clean_user_data(ldap_data):
    model_data = clean_user_data(ldap_data)

    # enabled_values = ['512', '544', '66048', '66080']
    # try:
    #     if model_data['is_active'] in enabled_values:
    #         model_data['is_active'] = True
    #     else:
    #         model_data['is_active'] = False
    # except KeyError:
    #     model_data['is_active'] = False


    return model_data




