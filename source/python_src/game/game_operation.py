if(__name__ == '__main__'):
    path = './source/python/rewrite'
    import os
    import sys
    print(os.path.abspath(path))
    sys.path.append(os.path.abspath(path))


from game.switch_page import *
from game.get_game_info import *
from game.identify_pages import *
from supports import *
from save_load import *

__all__ = ['ConfirmOperation', 'restart', 'goto_game_page', 'expedition',
           'DestoryShip', 'change_fight_map', 'MoveTeam', 'SetSupport',
           'QuickRepair', 'GainBounds', 'RepairByBath', 'SetAutoSupply', 'Supply',
           'ChangeShip', 'ChangeShips', ]


def ConfirmOperation(timer: Timer, must_confirm=0, delay=0.5, confidence=.9, timeout=0):
    """等待并点击弹出在屏幕中央的各种确认按钮

    Args:
        must_confirm (int, optional): 是否必须按. Defaults to 0.
        delay (float, optional): 点击后延时(秒). Defaults to 0.5.
        timeout (int, optional): 等待延时(秒),负数或 0 不等待. Defaults to 0.

    Raises:
        ImageNotFoundErr: 如果 must_confirm = True 但是 timeout 之内没找到确认按钮排除该异常
    Returns:
        bool:True 为成功,False 为失败
    """
    pos = WaitImages(timer, ConfirmImage[1:], confidence, timeout=timeout)
    if pos is None:
        if(must_confirm == 1):
            raise ImageNotFoundErr("no confirm image found")
        else:
            return False
    res = GetImagePosition(timer, ConfirmImage[pos + 1], 0)
    click(timer, res[0], res[1], delay=delay)
    return True


def restart(timer: Timer, TryTimes=0):
    """重新启动游戏(实现不优秀,需重写)

    Args:
        timer (Timer): _description_
        TryTimes (int, optional): _description_. Defaults to 0.

    Raises:
        NetworkErr: _description_
    """
    if(TryTimes > 4):
        print("Failed,Checking Error")
        if(CheckNetWork() == False):
            print("Catched,NetWorkError")
            print("Trying restart")
        else:
            raise NetworkErr()
    if(TryTimes > 2):
        print("Error:Couldn't start application")
        print("Try Restart Android")
        RestartAndroid(timer, TryTimes)
        ConnectAndroid(timer, 0)
        time.sleep(1)
        print("Checked,Trying")

    print("Restarting Game")
    ShellCmd(timer, "am force-stop com.huanmeng.zhanjian2")
    result = WaitImage(timer, StartImage[1])
    if(result == False and TryTimes > 10):
        print("Configration Error:Couldn't find application on desktop")
        time.sleep(100000)
    click(timer, result[0], result[1])
    if(S.LONGUSED == 1):
        ConfirmOperation(timer, 1, timeout=100)
    starttime = time.time()
    while True:
        if(time.time() - starttime >= 200):
            restart(timer, TryTimes + 1)
            return
        print("Waiting Start")
        type = WaitImages(timer, [StartImage[2]]+ConfirmImage[1:], TimeOut=60)
        print("Type Get:", type)
        if (type == 0):
            result = WaitImage(timer, StartImage[2], 0.9, 200)
            if (result != False):
                click(result[0], result[1])
            else:
                restart(TryTimes + 1)
            return
        else:
            print("Confirming")
            if(type != None):
                ConfirmOperation(timer)


def goto_game_page(timer: Timer, target='main'):
    """到某一个游戏界面

    Args:
        timer (Timer): _description_
        target (str, str): 目标章节名(见 ./constants/other_constants). Defaults to 'main'.
    """
    walk_to(timer, target)
    # wait_pages(timer, names=[timer.now_page.name])


@logit_time()
def expedition(timer: Timer, try_times=0):
    """检查远征,如果有未收获远征,则全部收获并用原队伍继续

    Args:
        timer (Timer): _description_
    """
    if(timer.now_page.name != 'map_page'):
        goto_game_page(timer, 'expedition_page')
    timer.expedition_status.update()
    if(timer.expedition_status.is_ready() == False):
        return try_times
    try:
        goto_game_page(timer, 'expedition_page')
        pos = WaitImage(timer, GameUI[6], timeout=2)
        click(timer, pos[0], pos[1], delay=1)
        WaitImage(timer, FightImage[3], after_get_delay=.25)
        click(timer, 900, 500, delay=1)
        ConfirmOperation(timer, must_confirm=1, delay=.5, confidence=.9)
    except:
        if(process_bad_network(timer, 'expedition')):
            pass
        raise ImageNotFoundErr("Unknown error led to this error")
    return expedition(timer, try_times + 1)


def DestoryShip(timer, reserve=1, amount=1):
    # amount:重要舰船的个数
    # 解装舰船
    walk_to(timer, 'destroy_page')

    WaitImage(timer, SymbolImage[5], after_get_delay=.33)
    click(timer, 301, 25)  # 这里动态延迟，点解装
    WaitImage(timer, SymbolImage[6], after_get_delay=.33)
    click(timer, 90, 206)  # 点添加
    WaitImage(timer, SymbolImage[7], after_get_delay=.33)
    # 进去
    click(timer, 877, 378, delay=1)

    click(timer, 544, 105, delay=0.33)
    click(timer, 619, 105, delay=0.33)
    click(timer, 624, 152, delay=0.33)
    click(timer, 537, 204, delay=0.33)
    click(timer, 851, 459, delay=0.33)
    # 筛出第一波

    for i in range(1, 8):
        click(timer, i * 100, 166, delay=0.33)
        click(timer, i * 100, 366, delay=0.33)
    # 选中第一波

    click(timer, 860, 480, delay=1)

    if(ImagesExist(timer, GameUI[8])):
        click(timer, 807, 346)
    click(timer, 870, 480, delay=1)
    click(timer, 364, 304, delay=0.66)
    # 清理第一波

    click(timer, 90, 206, delay=1)
    WaitImage(timer, SymbolImage[7], after_get_delay=.5)
    click(timer, 877, 378, delay=1)  # 点“类型”
    click(timer, 536, 62, delay=0.33)
    click(timer, 851, 459, delay=0.33)
    # 再进去并筛出第二波
    if(reserve == 1):
        click(timer, 853, 270, delay=0.66)
        click(timer, 579, 208, delay=0.66)
    # 是否解装小船
    for i in range(1, amount + 1):
        click(timer, i * 100, 166, delay=0.33)
    # 选中第二波

    click(timer, 860, 480, delay=0.66)
    click(timer, 870, 480, delay=1)
    if(ImagesExist(timer, GameUI[8])):
        click(807, 346)
    click(timer, 364, 304, delay=0.66)


def MoveChapter(timer: Timer, target, chapter_now=None):
    """移动地图章节到 target
    含错误检查

    Args:
        timer (Timer): _description_
        target (int): 目标
        chapter_now (_type_, optional): 现在的章节. Defaults to None.
    Raise:
        ImageNotFoundErr:如果没有找到章节标志或地图界面标志
    """
    if(identify_page(timer, 'map_page') == False):
        raise ImageNotFoundErr("not on page 'map_page' now")

    if(chapter_now == target):
        return
    try:
        if(chapter_now == None):
            chapter_now = GetChapter(timer)
        print("NowChapter:", chapter_now)
        if(chapter_now > target):
            if(chapter_now - target >= 3):
                chapter_now -= 3
                click(timer, 95, 97, delay=0)
            elif(chapter_now - target == 2):
                chapter_now -= 2
                click(timer, 95, 170, delay=0)
            elif(chapter_now - target == 1):
                chapter_now -= 1
                click(timer, 95, 229, delay=0)

            if(WaitImage(timer, ChapterImage[chapter_now]) == False):
                raise ImageNotFoundErr("after movechapter operation but the chapter do not move")
            time.sleep(0.15)
            MoveChapter(timer, target, chapter_now)
        else:
            if(chapter_now - target <= -3):
                chapter_now += 3
                click(timer, 95, 485, delay=0)
            elif(chapter_now - target == -2):
                chapter_now += 2
                click(timer, 95, 416, delay=0)
            elif(chapter_now - target == -1):
                chapter_now += 1
                click(timer, 95, 366, delay=0)

            if(WaitImage(timer, ChapterImage[chapter_now]) == False):
                raise ImageNotFoundErr("after movechapter operation but the chapter do not move")
            time.sleep(0.15)
            MoveChapter(timer, target, chapter_now)
    except Exception as exception:
        print("can't move chapter, time now is", time.time)
        if(process_bad_network(timer, 'move_chapter')):
            MoveChapter(timer, target)
        else:
            raise ImageNotFoundErr("unknow reason can't find chapter image")


def MoveNode(timer: Timer, target):
    """改变地图节点,不检查是否有该节点
    含网络错误检查
    Args:
        timer (Timer): _description_
        target (_type_): 目标节点

    """
    if(identify_page(timer, 'map_page') == False):
        raise ImageNotFoundErr("not on page 'map_page' now")

    NowNode = GetNode(timer)
    try:
        print("NowNode:", NowNode)
        if(target > NowNode):
            for i in range(1, target - NowNode + 1):
                swipe(timer, 715, 147, 552, 147, duration=0.25)
                if(WaitImage(timer, NumberImage[NowNode + i]) == False):
                    raise ImageNotFoundErr("after movechapter operation but the chapter do not move")
                time.sleep(0.15)
        else:
            for i in range(1, NowNode - target + 1):
                swipe(timer, 552, 147, 715, 147, duration=0.25)
                if(WaitImage(timer, NumberImage[NowNode - i]) == False):
                    raise ImageNotFoundErr("after movechapter operation but the chapter do not move")
                time.sleep(0.15)
    except:
        print("can't move chapter, time now is", time.time)
        if(process_bad_network(timer)):
            MoveNode(timer, target)
        else:
            raise ImageNotFoundErr("unknow reason can't find number image" + str(target))


def change_fight_map(timer: Timer, chapter, node):
    """在地图界面改变战斗地图(通常是为了出征)
    可以处理网络错误
    Args:
        timer (Timer): _description_
        chapter (int): 目标章节
        node (int): 目标节点

    Raises:
        ValueError: 不在地图界面
        ValueError: 不存在的节点
    """
    if(timer.now_page.name != 'map_page'):
        raise ValueError("can't change_fight_map at page:", timer.now_page.name)
    if node not in NODE_LIST[chapter]:
        raise ValueError('node' + str(node) + 'not in the list of chapter' + str(chapter))

    MoveChapter(timer, chapter)
    MoveNode(timer, node)
    timer.chapter = chapter
    timer.node = node


def vertify_team(timer: Timer):
    """检验目前是哪一个队伍(1~4)
    含网络状况处理
    Args:
        timer (Timer): _description_

    Raises:
        ImageNotFoundErr: 未找到队伍标志
        ImageNotFoundErr: 不在相关界面

    Returns:
        int: 队伍编号(1~4)
    """
    if(identify_page(timer, 'fight_prepare_page') == False):
        raise ImageNotFoundErr("not on fight_prepare_page")

    for i, position in enumerate([(64, 83), (186, 83), (310, 83), (430, 83)]):
        if(PixelChecker(timer, position, bgr_color=(228, 132, 16))):
            return i + 1
    if(process_bad_network(timer)):
        return vertify_team(timer)

    raise ImageNotFoundErr()


def MoveTeam(timer: Timer, target, try_times=0):
    """切换队伍
    Args:
        timer (Timer): _description_
        target (_type_): 目标队伍
        try_times: 尝试次数
    Raise:
        ValueError: 切换失败
        ImageNotFoundErr: 不在相关界面
    """
    if(try_times > 3):
        raise ValueError("can't change team sucessfully")
    if(identify_page(timer, 'fight_prepare_page') == False):
        raise ImageNotFoundErr("not on 'fight_prepare_page' ")

    if(vertify_team(timer) == target):
        return
    print("正在切换队伍到:", target)
    click(timer, 110 * target, 81)
    if(vertify_team(timer) != target):
        MoveTeam(timer, target, try_times + 1)


def SetSupport(timer: Timer, target, try_times=0):
    """启用战役支援

    Args:
        timer (Timer): _description_
        target (bool, int): 目标状态
    Raise:
        ValueError: 未能成功切换战役支援状态
    """
    target = bool(target)
    walk_to(timer, "fight_prepare_page")
    is_bad_network
    if(CheckSupportStatu() != target):
        click(timer, 628, 82, delay=1)
        click(timer, 760, 273, delay=1)
        click(timer, 480, 270, delay=1)
    if(is_bad_network(timer, 0) or CheckSupportStatu(timer) != target):
        if(process_bad_network(timer, 'set_support')):
            SetSupport(timer, target)
        else:
            raise ValueError("can't set right support")


def QuickRepair(timer: Timer, repair_logic=None, *args, **kwargs):
    """战斗界面的快速修理

    Args:
        timer (Timer): _description_
    """
    ShipStatu = DetectShipStatu(timer)
    broken = 0
    for x in ShipStatu[1:]:
        if(x != 0 and x != -1):
            broken = 1

    print("ShipStatu:", ShipStatu)
    if(broken >= 1 or ImagesExist(timer, RepairImage[1])):
        click(timer, 420, 420, delay=1.5)
        pos = GetImagePosition(timer, RepairImage[1])
        while(pos != None):
            click(timer, pos[0], pos[1], delay=1)
            pos = GetImagePosition(timer, RepairImage[1])
        for i in range(1, 7):
            if(ShipStatu[i] != 0 and ShipStatu[i] != -1):
                log_info(timer, "WorkInfo:" + str(kwargs))
                log_info(timer, str(i)+" Repaired")
                click(timer, BLOODLIST_POSITION[0][i][0], BLOODLIST_POSITION[0][i][1], delay=1.5)
        click(timer, 163, 420, delay=1)


def GainBounds(timer: Timer):
    """检查任务情况,如果可以领取奖励则领取

    Args:
        timer (Timer): _description_
    """
    goto_game_page(timer, 'mission_page')
    walk_to(timer, 'mission_page')
    if(ClickImage(timer, GameUI[15])):
        ConfirmOperation(timer, must_confirm=1)
    elif(ClickImage(timer, GameUI[12])):
        ConfirmOperation(timer, must_confirm=1)
    #click(timer, 774, 502)


def RepairByBath(timer: Timer):
    """使用浴室修理修理时间最长的单位

    Args:
        timer (Timer): _description_
    """
    walk_to(timer, 'choose_repair_page')
    click(timer, 115, 233)


def SetAutoSupply(timer: Timer, type=1):
    UpdateScreen(timer)
    NowType = int(PixelChecker(timer, (48, 508), (224, 135, 35)))
    if(NowType != type):
        click(timer, 44, 503, delay=0.33)


def Supply(timer: Timer, List=[1, 2, 3, 4, 5, 6], try_times=0):
    """补给指定舰船

    Args:
        timer (Timer): _description_
        List (list, optional): 补给舰船列表,可以为单个整数. Defaults to [1, 2, 3, 4, 5, 6].
        try_times (int, optional): _description_. Defaults to 0.

    Raises:
        ValueError: 补给失败
        TypeError: List 参数有误
    """
    if(try_times > 3):
        raise ValueError("can't supply ship")

    if(isinstance(List, int)):
        List = [List]

    click(timer, 293, 420)
    for x in List:
        if not isinstance(x, int):
            raise TypeError("ship must be represent as a int but get" + str(List))
        click(timer, 110 * x, 241)

    if(is_bad_network(timer, 0)):
        process_bad_network(timer, 'supply ships')
        Supply(timer, List, try_times + 1)


def ChangeShip(timer: Timer, team, pos=None, name=None, pre=None):

    if(team is not None):
        walk_to(timer, 'fight_prepare_page')
        MoveTeam(timer, team)
        if(team >= 5):
            # 切换为预设编队
            # 暂不支持
            return

    # 切换单船
    # 懒得做 OCR 所以默认第一个
    DetectShipStatu(timer)
    if(name == None and timer.ship_status[pos] == -1):
        return
    click(timer, 110 * pos, 250, delay=1.5)
    if(name == None):
        click(timer, 83, 167, delay=1)
        return

    click(timer, 700, 30, delay=0.5)
    text(name)
    click(timer, 50, 50, delay=0.5)
    if(timer.ship_status[pos] == -1):
        click(timer, 83, 167, delay=1)
    else:
        click(timer, 183, 167, delay=1)
    if(ImagesExist(timer, SymbolImage[7])):
        click(timer, 27, 30, delay=1)


def ChangeShips(timer: Timer, team, list):
    """更换编队舰船

    Args:
        team (int): 1~4,表示舰队编号
        list (舰船名称列表): 

    For instance:
        ChangeShips(timer, 2, [None, "萤火虫", "伏尔塔", "吹雪", "明斯克", None, None])

    """
    for i in range(6):
        ChangeShip(timer, team, 1, None)
    list = list + [None] * 6
    for i in range(1, 7):
        ChangeShip(timer, team, i, list[i])


def get_new_things(timer: Timer, lock=0):
    pass


if(__name__ == '__main__'):
    timer = Timer()
    load_all_data(timer)
    load_game_ui(timer)

    ConnectAndroid(timer)
    timer.expedition_status = ExpeditionStatus(timer)
    UpdateScreen(timer)
    timer.set_page(get_now_page(timer))
    print(timer.now_page.name)
    ChangeShips(timer, 4, ['U-47', 'U-81'])