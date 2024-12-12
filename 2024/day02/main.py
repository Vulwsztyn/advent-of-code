from pathlib import Path


def within_bounds(v, v2):
    return 0 < abs(v - v2) < 4


def consistent_with_increasing(v, prev_v, is_increasing):
    return (v > prev_v) == is_increasing


def is_array_ok_helper(arr, i, prev_i, is_increasing):
    if i >= len(arr):
        return True
    if not within_bounds(arr[i], arr[prev_i]) or not consistent_with_increasing(
        arr[i], arr[prev_i], is_increasing
    ):
        print(i, prev_i, is_increasing)
        print(f"wb: {within_bounds(arr[i], arr[prev_i])}, {arr[i]}, {arr[prev_i]}")
        print(consistent_with_increasing(arr[i], arr[prev_i], is_increasing))
        print(arr[i] > arr[prev_i])
        print(is_increasing)
        print((arr[i] > arr[prev_i]) == is_increasing)
        return False
    return is_array_ok_helper(arr, i + 1, i, is_increasing)


def is_array_ok(arr):
    return is_array_ok_helper(arr, 1, 0, arr[1] > arr[0])


def is_array_ok_with_mistake_helper(arr, i, prev_i, is_increasing):
    if i >= len(arr) - 1:
        return True
    is_ok = within_bounds(arr[i], arr[prev_i]) and consistent_with_increasing(
        arr[i], arr[prev_i], is_increasing
    )
    if is_ok:
        return is_array_ok_with_mistake_helper(arr, i + 1, i, is_increasing)
    print(f"mistake found at index: {i}")
    if i == 1:
        return is_array_ok_helper(arr, 2, 0, arr[2] > arr[0]) or is_array_ok_helper(
            arr, 2, 1, arr[2] > arr[1]
        )
    if i == 2:
        return (
            is_array_ok_helper(arr, 3, 1, is_increasing)
            or (
                within_bounds(arr[2], arr[0])
                and is_array_ok_helper(arr, 3, 2, arr[2] > arr[0])
            )
            or (
                within_bounds(arr[2], arr[1])
                and is_array_ok_helper(arr, 3, 2, arr[2] > arr[1])
            )
        )
    return is_array_ok_helper(arr, i + 1, prev_i, is_increasing) or is_array_ok_helper(
        arr, i, prev_i - 1, is_increasing
    )


def is_array_ok_with_mistake(arr):
    return is_array_ok_with_mistake_helper(arr, 1, 0, arr[1] > arr[0])


file = Path("data.txt")
text = file.read_text()
result = 0
for i, v in enumerate(text.split("\n")):
    if not v:
        break
    if is_array_ok([int(x) for x in v.split(" ")]):
        result += 1
print(result)

result = 0
for i, v in enumerate(text.split("\n")):
    # if i<20:
    #     continue
    if not v:
        break
    print(v)
    is_ok = is_array_ok_with_mistake([int(x) for x in v.split(" ")])
    print(is_ok)
    print()
    if is_ok:
        result += 1

    # if i>30:
    #     break
# for i, v in enumerate(text.split("\n")):
#     if not v:
#         break
#     is_ok1 = is_array_ok([int(x) for x in v.split(" ")])
#     is_ok2 = is_array_ok_with_mistake([int(x) for x in v.split(" ")])
#     if is_ok1 != is_ok2:
#         print(v)
#         print(is_ok1, is_ok2)
print(result)
