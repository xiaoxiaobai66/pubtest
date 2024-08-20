#日志封装器
#loggers日志器： 程序的入口 别的文件想要调用就用日志器
#handlers处理器： 日志信息 输出到你想要的位置 控制台处理器  文本处理器
#formatter 格式器：处理日志格式  格式比较好看
#filter 过滤器
import logging
import time


def test_log2():
    #logging---创建日志器时使用  logger调用日志信息时使用
    #创建日志器 这个日志器就写入了日志信息
    logger=logging.getLogger()
    #日志信息全面 设置日志级别
    logger.setLevel(logging.INFO)  #一般使用INFO  DEBUG日志信息过于冗余
    #日志信息显示在控制台-- 判断是否已经存在处理器 没有才创建：
    # 场景：如果没有这个限制只要有一个以上的模块创建了日志实例，就会出现同一条日志重复打印
    if not logger.handlers:  #一加了这个判断后 没有日志生成、控制台也不展示了 ，暂将判断注释，下面代码恢复缩进
        #最后可以，错误原因：return logger一起加了个tab位  导致什么都没有回显出来
        # --需要控制台处理器
        sh=logging.StreamHandler()
        #日志信息放入控制台中
        logger.addHandler(sh)

        # 生成时间戳用于测试报告
        time_now = time.strftime('%Y%m%d', time.localtime(time.time()))
        #保存在文件中 文件处理器
        fh=logging.FileHandler(fr".\key_log\log\{time_now}.txt",encoding="utf-8")

        #日志信息放入文件中
        logger.addHandler(fh)

        #日志比较丑：设置格式 创建格式器
        fmt='%(asctime)s %(levelno)s %(levelname)s %(funcName)s %(message)s'
        geshi1=logging.Formatter(fmt)

        #给控制台加格式  给文本日志加格式
        sh.setFormatter(geshi1)
        fh.setFormatter(geshi1)

    return logger

# logger.debug("调试")
# logger.info("正常")
# logger.warning("警告")
# logger.error("错误")
# logger.critical("崩溃")