#include <unordered_set>


template <class type> type get_element(unordered_set<type> non_empty_set) {
	for (type object: non_empty_set) {
		return object;
	}

	throw runtime_error("get_element called on an empty set.");
}


template <class type> unordered_set<type> intersection_set(unordered_set<type> first, unordered_set<type> second) {
	unordered_set<type> output{};
	for (type object: first) {
		if (second.find(object) != second.end()) {
			output.insert(object);
		}
	}

	return output;
}


template <class type> unordered_set<type> union_set(unordered_set<type> first, unordered_set<type> second) {
	unordered_set<type> output{};
	for (type object: first) {
		output.insert(object);
	}
	for (type object: second) {
		output.insert(object);
	}

	return output;
}


template <class type> unordered_set<type> difference_set(unordered_set<type> first, unordered_set<type> second) {
	unordered_set<type> output{};
	for (type object: first) {
		if (second.find(object) == second.end()) {
			output.insert(object);
		}
	}

	return output;
}
