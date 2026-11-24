# 이산수학 Report 2 - 집합 A = {1, 2, 3, 4, 5} 동치 관계 판별 프로그램

SET_A = [1, 2, 3, 4, 5]
SIZE = 5


def show_matrix(mat, label="관계 행렬"):
    print(f"\n[{label}]")
    print("     " + "  ".join(str(x) for x in SET_A))
    print("   +" + "-" * (SIZE * 3 + 1))
    for r in range(SIZE):
        line = "  ".join(str(mat[r][c]) for c in range(SIZE))
        print(f" {SET_A[r]} |  {line}")


def read_matrix():
    """[조건 1] 5x5 정방행렬을 행 단위로 입력받아 2차원 리스트로 저장"""
    print("--------------------------------------------------")
    print(" 집합 A = {1, 2, 3, 4, 5} 관계 행렬 입력 (5x5)")
    print(" 각 행마다 0 또는 1을 5개 입력하세요. (예: 1 0 1 0 1)")
    print("--------------------------------------------------")
    mat = []
    for r in range(SIZE):
        while True:
            text = input(f" {r + 1}번째 행: ").strip()
            parts = list(text) if (" " not in text and len(text) == SIZE) else text.split()
            if len(parts) != SIZE or any(p not in ("0", "1") for p in parts):
                print("  -> 잘못된 입력입니다. 0 또는 1을 정확히 5개 입력해주세요.")
                continue
            mat.append([int(p) for p in parts])
            break
    return mat


def check_reflexive(mat):
    """[조건 2-1] 반사 관계 판별"""
    missing = [SET_A[i] for i in range(SIZE) if mat[i][i] != 1]
    return len(missing) == 0, missing


def check_symmetric(mat):
    """[조건 2-2] 대칭 관계 판별"""
    missing = []
    for i in range(SIZE):
        for j in range(SIZE):
            if mat[i][j] == 1 and mat[j][i] == 0:
                missing.append((SET_A[i], SET_A[j]))
    return len(missing) == 0, missing


def check_transitive(mat):
    """[조건 2-3] 추이 관계 판별"""
    missing = []
    for i in range(SIZE):
        for j in range(SIZE):
            if mat[i][j] == 1:
                for k in range(SIZE):
                    if mat[j][k] == 1 and mat[i][k] == 0:
                        pair = (SET_A[i], SET_A[k])
                        if pair not in missing:
                            missing.append(pair)
    return len(missing) == 0, missing


def evaluate_relation(mat):
    """[조건 2] 세 성질 판별 및 동치 관계 여부 출력"""
    r_ok, r_miss = check_reflexive(mat)
    s_ok, s_miss = check_symmetric(mat)
    t_ok, t_miss = check_transitive(mat)

    print("\n[성질 판별 결과]")
    print(f" * 반사 관계: {'성립' if r_ok else f'불성립 (누락 대각 원소: {r_miss})'}")
    print(f" * 대칭 관계: {'성립' if s_ok else f'불성립 (단방향 쌍: {s_miss[:3]})'}")
    print(f" * 추이 관계: {'성립' if t_ok else f'불성립 (누락 연결 쌍: {t_miss[:3]})'}")

    is_equiv = r_ok and s_ok and t_ok
    if is_equiv:
        print(" => 판정: 입력된 관계는 동치 관계입니다.")
    else:
        print(" => 판정: 입력된 관계는 동치 관계가 아닙니다.")
    return is_equiv, r_ok, s_ok, t_ok


def find_equiv_classes(mat):
    """[조건 3] 각 원소에 대한 동치류 판별"""
    classes = {}
    for i in range(SIZE):
        classes[SET_A[i]] = [SET_A[j] for j in range(SIZE) if mat[i][j] == 1]
    return classes


def show_equiv_classes(mat):
    """[조건 3] 원소별 동치류 및 분할(A/R) 출력"""
    classes = find_equiv_classes(mat)
    print("\n[원소별 동치류]")
    for x in SET_A:
        vals = ", ".join(str(v) for v in classes[x])
        print(f"  [{x}] = {{{vals}}}")

    # 추가기능: 중복 제거된 분할 집합 A/R 출력
    partitions = []
    for x in SET_A:
        grp = tuple(classes[x])
        if grp not in partitions:
            partitions.append(grp)
    part_text = ", ".join("{" + ", ".join(map(str, g)) + "}" for g in partitions)
    print(f"  => 동치 분할(A/R) = {{{part_text}}}")


def show_adj_list(mat):
    """[추가기능] 유향 그래프 인접 리스트 출력"""
    print("\n[인접 리스트 표현]")
    for i in range(SIZE):
        adj = [str(SET_A[j]) for j in range(SIZE) if mat[i][j] == 1]
        print(f"  {SET_A[i]} -> {{{', '.join(adj)}}}")


def diff_added_pairs(before, after):
    """[추가기능] 폐포 변환으로 새로 추가된 순서쌍 추출"""
    added = []
    for i in range(SIZE):
        for j in range(SIZE):
            if before[i][j] == 0 and after[i][j] == 1:
                added.append((SET_A[i], SET_A[j]))
    return added


def make_reflexive_closure(mat):
    """[조건 4-1] 반사 폐포"""
    res = [row[:] for row in mat]
    for i in range(SIZE):
        res[i][i] = 1
    return res


def make_symmetric_closure(mat):
    """[조건 4-2] 대칭 폐포"""
    res = [row[:] for row in mat]
    for i in range(SIZE):
        for j in range(SIZE):
            if res[i][j] == 1:
                res[j][i] = 1
    return res


def make_transitive_closure(mat):
    """[조건 4-3] 추이 폐포 (Warshall 알고리즘)"""
    res = [row[:] for row in mat]
    for k in range(SIZE):
        for i in range(SIZE):
            for j in range(SIZE):
                if res[i][k] == 1 and res[k][j] == 1:
                    res[i][j] = 1
    return res


def make_equiv_closure(mat):
    """[추가기능] 반사 -> 대칭 -> 추이 폐포를 순차 적용한 통합 동치 폐포"""
    step1 = make_reflexive_closure(mat)
    step2 = make_symmetric_closure(step1)
    step3 = make_transitive_closure(step2)
    return step3


def run_closure_step(name, orig_mat, closed_mat):
    print("\n" + "=" * 50)
    print(f"  [{name} 변환 결과]")
    show_matrix(orig_mat, f"{name} 변환 전")
    show_matrix(closed_mat, f"{name} 변환 후")
    added = diff_added_pairs(orig_mat, closed_mat)
    print(f"  * 새로 추가된 원소: {added if added else '없음'}")
    ok, _, _, _ = evaluate_relation(closed_mat)
    if ok:
        show_equiv_classes(closed_mat)


def main():
    mat = read_matrix()
    show_matrix(mat, "입력한 관계 행렬")
    show_adj_list(mat)

    is_equiv, r_ok, s_ok, t_ok = evaluate_relation(mat)
    if is_equiv:
        show_equiv_classes(mat)
    else:
        if not r_ok:
            run_closure_step("반사 폐포", mat, make_reflexive_closure(mat))
        if not s_ok:
            run_closure_step("대칭 폐포", mat, make_symmetric_closure(mat))
        if not t_ok:
            run_closure_step("추이 폐포", mat, make_transitive_closure(mat))

        # 추가기능: 통합 동치 폐포
        eq_mat = make_equiv_closure(mat)
        run_closure_step("통합 동치 폐포(추가기능)", mat, eq_mat)


if __name__ == "__main__":
    main()