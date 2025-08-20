"""
비현실적인 수익률 체크 스크립트
"""

import os
import re
import glob

def check_unrealistic_profits(file_path):
    """파일에서 비현실적인 수익률 찾기"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    filename = os.path.basename(file_path)
    
    # 1. 50% 이상 수익률 체크
    profit_patterns = [
        (r'(\d{2,3})%\s*수익', '수익률'),
        (r'(\d{2,3})%\s*마진', '마진율'),
        (r'순이익률.*?(\d{2,3})%', '순이익률'),
        (r'순익.*?(\d{2,3})%', '순익률'),
    ]
    
    for pattern, label in profit_patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            try:
                value = int(match.group(1))
                if value > 40:  # 40% 초과는 비현실적
                    line_num = content[:match.start()].count('\n') + 1
                    issues.append({
                        'file': filename,
                        'line': line_num,
                        'issue': f'{label} {value}%',
                        'text': match.group(0)
                    })
            except:
                pass
    
    # 2. 매출 대비 순익 체크 (예: 200만원 매출에 120만원 순익)
    revenue_profit_patterns = [
        r'매출.*?(\d+).*?순익.*?(\d+)',
        r'월.*?(\d+)만원.*?순.*?(\d+)만원',
    ]
    
    for pattern in revenue_profit_patterns:
        matches = re.finditer(pattern, content, re.DOTALL)
        for match in matches:
            try:
                revenue = int(match.group(1))
                profit = int(match.group(2))
                if profit > revenue * 0.4:  # 순익이 매출의 40% 초과
                    line_num = content[:match.start()].count('\n') + 1
                    issues.append({
                        'file': filename,
                        'line': line_num,
                        'issue': f'매출 {revenue} 대비 순익 {profit} (비율: {profit/revenue*100:.0f}%)',
                        'text': match.group(0)[:100]
                    })
            except:
                pass
    
    # 3. 특정 문제 패턴 체크
    problem_patterns = [
        (r'김.*?OO.*?200.*?120', '김OO님 사례 문제'),
        (r'월\s*순수익.*?(\d{3,4})만원', '과도한 순수익'),
    ]
    
    for pattern, desc in problem_patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            issues.append({
                'file': filename,
                'line': line_num,
                'issue': desc,
                'text': match.group(0)
            })
    
    return issues

def main():
    base_path = r'C:\bid\ebook'
    all_issues = []
    
    # HTML 파일 검사
    html_files = glob.glob(os.path.join(base_path, '*.html'))
    
    for file_path in html_files:
        issues = check_unrealistic_profits(file_path)
        all_issues.extend(issues)
    
    # 결과 출력
    if all_issues:
        print(f"\n총 {len(all_issues)}개 문제 발견:\n")
        for issue in all_issues:
            print(f"파일: {issue['file']}")
            print(f"  라인: {issue['line']}")
            print(f"  문제: {issue['issue']}")
            print(f"  내용: {issue['text'][:50]}...")
            print()
    else:
        print("비현실적인 수익률 문제를 찾지 못했습니다.")

if __name__ == "__main__":
    main()