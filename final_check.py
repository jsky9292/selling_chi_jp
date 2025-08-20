"""
최종 검증 스크립트 - 오타, 비현실적 데이터, 특정 업체명 점검
"""

import os
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
        ]
        
        for pattern, msg in company_checks:
            if pattern.lower() in content.lower():
                # A사 배대지는 제외
                if 'A사 배대지' not in content or pattern.lower() != 'bidbuy':
                    issues.append(f"[경고] {msg}: {pattern}")
        
        # 2. 비현실적인 수익률 체크
        profit_patterns = [
            (r'(\d{2,3})%\s*수익', '수익률'),
            (r'(\d{2,3})%\s*마진', '마진율'),
            (r'순이익률.*?(\d{2,3})%', '순이익률'),
        ]
        
        for pattern, label in profit_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                try:
                    value = int(match.group(1))
                    if value > 50:  # 50% 초과는 비현실적
                        issues.append(f"[경고] 비현실적 {label}: {value}%")
                except:
                    pass
        
        # 3. 오타 체크
        typo_checks = [
            ('메르카리', '메루카리'),
            ('알리마마', '알리바바'),
            ('카카오', '카카오 제거 필요'),
        ]
        
        for wrong, correct in typo_checks:
            if wrong in content:
                issues.append(f"[오타] '{wrong}' -> '{correct}'로 수정 필요")
        
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
        print(f"  [오류] {e}")
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
        print(f"\n[경고] 문제가 발견된 파일: {len(files_with_issues)}개")
        for filename in files_with_issues:
            print(f"\n파일: {filename}")
            for issue in all_issues[filename]:
                print(f"    {issue}")
        
        print("\n[중요] Git 업로드 전 위 문제들을 수정해야 합니다.")
    else:
        print("\n[성공] 모든 파일이 검증을 통과했습니다!")
        print("[정보] Git에 업로드 가능합니다.")
    
    print("\n" + "=" * 60)
    print("최종 업로드 파일 목록:")
    print("=" * 60)
    for filename in files_to_check:
        if os.path.exists(os.path.join(base_path, filename)):
            status = "[OK]" if filename not in files_with_issues else "[수정필요]"
            print(f"{status} {filename}")

if __name__ == "__main__":
    main()