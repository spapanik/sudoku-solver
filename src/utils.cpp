#include <string>
#include <regex>

#include "utils.hpp"

using namespace ::std;

const regex expression("[^1-9]");

string clean_string(char* initial){
	return regex_replace(initial, expression, ".");
}
