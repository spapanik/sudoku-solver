#include <unordered_set>
#include <vector>

using namespace ::std;

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


template <class container, class type> class Combinations {
	vector<int> state;
	vector<type> objects;
	int length;
	int choose;

	public:
		Combinations(container iterable, int choose):
			choose(choose) {
				length = 0;
				for (type elem: iterable) {
					objects.push_back(elem);
					length++;
				}
				for (int i = 0; i < choose; i++) {
					state.push_back(i);
				}
				completed = (length == 0 || choose > length);
			}

		bool completed;
		vector<type> next() {
			vector<type> out;
			for (int i: state) {
				out.push_back(objects[i]);
			}

			completed = true;
			for (int i = choose - 1; i >= 0; --i) {
				if (state[i] < length - choose + i) {
					int j = state[i] + 1;
					while (i <= choose - 1) {
						state[i++] = j++;
					}
					completed = false;
					break;
				}
			}

			return out;
		}
};
