BLOODLIST_POSITION = [[[], [56, 322], [168, 322], [280, 322], [392, 322], [504, 322], [616, 322]],
                      [[], [60, 142], [60, 217], [60, 292], [60, 367], [60, 442], [60, 517]]]  # 血条的坐标

POINT_POSITION = {}  # 战斗点位(1-1A 中的 'A') 的坐标
TYPE_SCAN_AREA = [[(277, 312, 309, 328), (380, 312, 412, 328), (483, 312, 515, 328),
                   (587, 312, 619, 328), (690, 312, 722, 328), (793, 312, 825, 328)],
                  [(39, 156, 71, 172), (322, 156, 354, 172), (39, 245, 71, 261),
                  (322, 245, 354, 261), (39, 334, 71, 350), (322, 334, 354, 350)]]
"""扫描舰船类型的区域
    [0] 表示演习的扫描区域
    [1] 表示索敌界面的扫描区域
    每个列表的六个四元组为 (left, top, right, buttom)
"""

FIGHT_CONDITIONS_POSITON = [None, (207, 221), (443, 287), (752, 196), (191, 413), (733, 400)]