#include <iostream>
#include <tuple>
#include <vector>
#include <unordered_map>

// Note: Remember to use g++, not gcc!

std::pair<std::size_t, std::size_t> two_sum(const std::vector<int>& numbers, int target) {
    std::unordered_map<int, std::size_t> index;
    for (size_t i = 0; i < numbers.size(); i++) {
        int num = numbers[i];
        if (target - num >= 0 && index.find(target - num) != index.end())
            return {i, index[target - num]};
        index[num] = i;
    }
    return {0, 0};
}

std::tuple<std::size_t, std::size_t, std::size_t> three_sum(const std::vector<int>& numbers, int target) {
    std::unordered_map<int, std::size_t> index;
    for (size_t i = 0; i < numbers.size(); i++) {
        for (size_t j = 0; j < numbers.size(); j++) {
            int num1 = numbers[i];
            int num2 = numbers[j];
            int diff = target - num1 - num2;
            if (diff >= 0 && index.find(diff) != index.end())
                return {i, j, index[diff]};
            index[num1] = i;
            index[num2] = j;
        }
    }
    return {0, 0, 0};
}

int main() {
    std::vector<int> nums;
    int num;
    while (std::cin >> num)
        nums.emplace_back(num);

    auto [a, b] = two_sum(nums, 2020);
    std::cout << nums[a] * nums[b] << std::endl;
    auto [i, j, k] = three_sum(nums, 2020);
    std::cout << nums[i] * nums[j] * nums[k] << std::endl;
    
    return 0;
}
