import logging

logger = logging.getLogger(__name__)

def process_header_row(header_params: dict, total_columns: int = 8) -> list:
    """
    处理表头行，返回特殊第一行的数据
    
    输入：
        - header_params: {
            "mawb_no": "16003279161",
            "flight_no": "CX509",
            "arrival_date": "20251210"
        }
        - total_columns: 总列数（默认8，对应A-H列）
    
    输出：
        - 返回列表格式：["", "MAWB NO：{值}", "", "", "FLIGHT NO：{值}", "", "", "ARRIVAL DATE：{值}"]
    """
    try:
        logger.info("开始处理表头行")
        
        mawb_no = header_params.get('mawb_no', '')
        flight_no = header_params.get('flight_no', '')
        arrival_date = header_params.get('arrival_date', '')
        
        # 初始化全空列表，长度为total_columns
        header_row = [''] * total_columns
        
        # 填充特定列的值（0-based索引）
        # B列 = 索引1
        if mawb_no and 1 < total_columns:
            header_row[1] = f"MAWB NO：{mawb_no}"
            logger.info(f"列B (索引1): MAWB NO：{mawb_no}")
        
        # E列 = 索引4
        if flight_no and 4 < total_columns:
            header_row[4] = f"FLIGHT NO：{flight_no}"
            logger.info(f"列E (索引4): FLIGHT NO：{flight_no}")
        
        # H列 = 索引7
        if arrival_date and 7 < total_columns:
            header_row[7] = f"ARRIVAL DATE：{arrival_date}"
            logger.info(f"列H (索引7): ARRIVAL DATE：{arrival_date}")
        
        logger.info(f"表头行处理完成 - 返回列表: {header_row}")
        
        return header_row
        
    except Exception as e:
        logger.error(f"处理表头行失败：{str(e)}", exc_info=True)
        raise


def fill_mawb_no(mawb_no: str) -> str:
    """
    填充MAWB NO
    
    输入：
        - mawb_no: MAWB NO值
    
    输出：
        - 格式化后的字符串："MAWB NO：{值}"
    """
    return f"MAWB NO：{mawb_no}"


def fill_flight_no(flight_no: str) -> str:
    """
    填充FLIGHT NO
    
    输入：
        - flight_no: FLIGHT NO值
    
    输出：
        - 格式化后的字符串："FLIGHT NO：{值}"
    """
    return f"FLIGHT NO：{flight_no}"


def fill_arrival_date(arrival_date: str) -> str:
    """
    填充ARRIVAL DATE
    
    输入：
        - arrival_date: ARRIVAL DATE值
    
    输出：
        - 格式化后的字符串："ARRIVAL DATE：{值}"
    """
    return f"ARRIVAL DATE：{arrival_date}"
