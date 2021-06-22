from ldap3 import Server, Connection, ALL, SUBTREE, LEVEL
import logging
import sys
import os



logger = logging.getLogger(__name__)




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
        logger.info(f'ldap_check_user_is_active: connection fail {type(conn).__name__ }.')
        return status
    if ldap_user_login is None or ldap_dc1 is None or ldap_dc2 is None or ldap_dc3 is None: 
        logger.info(f'ldap_check_user_is_active: params fail.')
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
        logger.info(f'ldap_check_user_exists_in_group: connection fail {type(conn).__name__ }.')
        return status
    if ldap_user_login is None or ldap_search_group is None or ldap_dc1 is None or ldap_dc2 is None or ldap_dc3 is None: 
        logger.info(f'ldap_check_user_exists_in_group: params fail.')
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
