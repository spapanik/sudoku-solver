#pragma once

#include <string>
#include <unordered_set>

using namespace ::std;

string clean_string(char *initial);

template <class type> type get_element(unordered_set<type> non_empty_set);
template <class type> unordered_set<type> intersection_set(unordered_set<type> first, unordered_set<type> second);
template <class type> unordered_set<type> union_set(unordered_set<type> first, unordered_set<type> second);
template <class type> unordered_set<type> difference_set(unordered_set<type> first, unordered_set<type> second);
#include "utils.template.cpp"
