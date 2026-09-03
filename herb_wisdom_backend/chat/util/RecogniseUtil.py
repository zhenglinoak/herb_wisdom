import json
import re
from ai import LoadIntentRecognitionModel


def intention_recognition(question):
    llm = LoadIntentRecognitionModel.load_intent_recognition_model()

    intention_prompt = """
        你是中医医疗意图识别器。
        【硬性强制规则】
        1. 禁止输出任何解释、问候、闲聊、前置后置文字！
        2. 只允许输出一段纯净JSON，除此之外不能有任何字符。
        3. 绝对不要反问用户，不要让用户提供内容，直接根据当前用户提问输出结果。
        
        # 判断定义：医疗/中医相关
        包括：疾病症状咨询、中药材/偏方/食疗功效用法、养生调理、中医理论、用药康复相关。
        
        # 非医疗
        纯情绪倾诉、闲聊、编程、生活琐事、娱乐、和身体健康无关话题。
        
        # 输出格式（严格遵守，只能返回如下结构JSON）
        {
            "is_medical": true/false,
            "confidence": "high/medium/low"
        }
        
        # 示例
        User: "大夫，我最近痔疮出血，有什么偏方吗？"
        {"is_medical": true, "confidence": "high"}
        
        User: "Python怎么读取Excel文件"
        {"is_medical": false, "confidence": "high"}
        """

    rs = llm.invoke([
        {"role": "system", "content": intention_prompt},
        {"role": "user", "content": question}
    ])

    content = rs.content.strip()

    # 步骤1：清除markdown ```json 标记
    if content.startswith("```json"):
        content = re.sub(r"```json|```", "", content).strip()

    # 步骤2：正则精准提取 {} 包裹的JSON字符串（核心！解决模型乱加文字）
    json_match = re.search(r"\{.*?\}", content, re.S)
    if json_match:
        json_str = json_match.group()
        try:
            result = json.loads(json_str)
            # 简单校验字段完整性
            if "is_medical" in result and "confidence" in result:
                return result
        except Exception as e:
            print("JSON解析失败：", e)

    # 步骤3：兜底策略，解析失败默认返回
    print("LLM未输出合法JSON，启用兜底返回")
    return {
        "is_medical": False,
        "confidence": "low"
    }


if __name__ == '__main__':
    res = intention_recognition("我刚刚问了啥")
    print("最终识别结果：", res)
    print(res["is_medical"])