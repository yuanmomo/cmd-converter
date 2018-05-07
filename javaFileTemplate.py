#!/usr/bin/env python
# encoding: utf-8


"This is a module of "

"""
@version    :   1.0
@author     :   MoMo
@license    :   Apache Licence 
@contact    :   yuanhongbin9090@gmail.com
@site       :   http://yuanmomo.net
@software   :   PyCharm
@file       :   java-file-template.py
@time       :   04/01/2018 12:40
"""

import sys
import os

header = """
package com.shy.server.netty.common.dto.%s;

import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

import com.shy.server.netty.common.cmd.CMD;
import com.shy.server.netty.common.constant.CType;
import com.shy.server.netty.common.dto.%s;
import com.shy.server.netty.common.dto.util.Type;

/**
 * Created by Hongbin.Yuan on 2018-01-03 15:01.
 */
@Component
public class %sCMD extends %s {

    public %sCMD() {
        super(CMD.Info.%s, CMD.Info.PARA.%s);
    }
"""

bodyTemplate="""

    @Type(name = "%s", type = CType.%s, order = %s)
    private %s %s;
"""

foot="""    
}
"""

if __name__ == '__main__':
    pass