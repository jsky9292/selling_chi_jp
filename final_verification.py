"""
최종 검증 스크립트 - 오타, 비현실적 데이터, 특정 업체명 점검
"""

import os
import glob
import re

def verify_file(file_path):
    """파일 내용 최종 검증"""
    filename = os.path.basename(file_path)
    print(f"\n검증 중: {filename}")
    print("-" * 50)
    
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. 특정 업체명 체크
        company_checks = [
            ('BiDBuy', '특정 업체명 발견'),
            ('bidbuy', '특정 업체명 발견'),
            ('비드바이', '특정 업체명 발견'),
            ('46,222', '특정 데이터 발견'),
            ('46222', '특정 데이터 발견'),
        ]
        
        for pattern, msg in company_checks:
            if pattern.lower() in content.lower():
                issues.append(f"[WARNING] {msg}: {pattern}")
        
        # 2. 비현실적인 수익률 체크
        profit_patterns = [
            (r'(\d{2,3})%\s*수익', '수익률'),
            (r'(\d{2,3})%\s*마진', '마진율'),
            (r'순이익률.*?(\d{2,3})%', '순이익률'),
            (r'ROAS.*?([4-9]\d{2}|[1-9]\d{3,})%', 'ROAS'),
            (r'전환율.*?([1-9]\d)%', '전환율'),
        ]
        
        for pattern, label in profit_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                try:
                    value = int(match.group(1))
                    if label in ['수익률', '마진율', '순이익률'] and value > 40:
                        issues.append(f"[WARNING] 비현실적 {label}: {value}%")
                    elif label == 'ROAS' and value > 400:
                        issues.append(f"[WARNING] 비현실적 ROAS: {value}%")
                    elif label == '전환율' and value > 10:
                        issues.append(f"[WARNING] 비현실적 전환율: {value}%")
                except:
                    pass
        
        # 3. 매출 대비 수익 체크
        unrealistic_patterns = [
            r'(\d+)만원\s*매출.*?(\d+)만원\s*수익',
            r'월\s*매출\s*(\d+).*?월\s*순수익\s*(\d+)',
        ]
        
        for pattern in unrealistic_patterns:
            matches = re.finditer(pattern, content, re.DOTALL)
            for match in matches:
                try:
                    revenue = int(match.group(1))
                    profit = int(match.group(2))
                    if profit > revenue * 0.4:  # 수익이 매출의 40% 초과
                        issues.append(f"[WARNING] 비현실적 수익: 매출 {revenue}만원, 수익 {profit}만원")
                except:
                    pass
        
        # 4. 오타 체크
        typo_checks = [
            ('컨텐츠', '콘텐츠'),
            ('어플리케이션', '애플리케이션'),
            ('어플', '앱'),
            ('유저', '사용자'),
            ('데이타', '데이터'),
            ('메르카리', '메루카리'),
            ('알리마마', '알리바바'),
            ('엔화', '엔'),
            ('위완화', '위안'),
            ('퍼센트', '%'),
        ]
        
        for wrong, correct in typo_checks:
            if wrong in content:
                issues.append(f"[TYPO] 오타: '{wrong}' -> '{correct}'로 수정 필요")
        
        # 5. 일관성 체크
        inconsistency_checks = [
            ('사업자등록', '사업자 등록'),
            ('온라인쇼핑몰', '온라인 쇼핑몰'),
            ('구매대행사업', '구매대행 사업'),
        ]
        
        for wrong, correct in inconsistency_checks:
            if wrong in content and correct not in content:
                issues.append(f"[TYPO] 띄어쓰기: '{wrong}' -> '{correct}'로 통일 필요")
        
        # 6. 숫자 데이터 신뢰성 체크
        if '1000만원' in content and '3000만원' in content:
            context = content[content.find('1000만원'):content.find('1000만원')+200]
            if '수익' in context or '이익' in context:
                issues.append(f"[WARNING] 수익 데이터 재확인 필요")
        
        # 결과 출력
        if issues:
            print(f"발견된 문제: {len(issues)}개")
            for issue in issues:
                print(f"  {issue}")
            return False, issues
        else:
            print("  [OK] 문제 없음")
            return True, []
            
    except Exception as e:
        print(f"  [ERROR] 오류: {e}")
        return False, [str(e)]

def main():
    base_path = r'C:\bid\ebook'
    
    # 검증할 주요 파일들
    files_to_check = [
        'guide_main_k7n2p9.html',
        'foundation_m3w8x5.html',
        'operation_j9v4t2.html',
        'marketing_p6d1s8.html',
        'legal_tax_r2h7y3.html',
        'automation_f5k9n1.html',
        'index.html',
        'intro_guide_a8f3k2.html',
        'revenue_model_x9m7p5.html',
        'advanced_strategy_h4b2n8.html',
        'legal_tax_guide_q3w6e1.html',
        'global_expansion_v7k4d9.html',
    ]
    
    print("=" * 60)
    print("최종 검증 시작")
    print("=" * 60)
    
    all_issues = {}
    files_with_issues = []
    
    for filename in files_to_check:
        file_path = os.path.join(base_path, filename)
        if os.path.exists(file_path):
            is_clean, issues = verify_file(file_path)
            if not is_clean:
                files_with_issues.append(filename)
                all_issues[filename] = issues
    
    print("\n" + "=" * 60)
    print("검증 결과 요약")
    print("=" * 60)
    
    if files_with_issues:
        print(f"\n[WARNING] 문제가 발견된 파일: {len(files_with_issues)}개")
        for filename in files_with_issues:
            print(f"\n[FILE] {filename}:")
            for issue in all_issues[filename]:
                print(f"    {issue}")
        
        print("\n[!] Git 업로드 전 위 문제들을 수정해야 합니다.")
    else:
        print("\n[OK] 모든 파일이 검증을 통과했습니다!")
        print("[OK] Git에 업로드 가능합니다.")
    
    print("\n" + "=" * 60)
    print("최종 업로드 파일 목록:")
    print("=" * 60)
    for filename in files_to_check:
        if os.path.exists(os.path.join(base_path, filename)):
            status = "[OK]" if filename not in files_with_issues else "[WARNING]"
            print(f"{status} {filename}")

if __name__ == "__main__":
    main()