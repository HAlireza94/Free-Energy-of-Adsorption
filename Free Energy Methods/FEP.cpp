#include <iostream>
#include <sstream>
#include <fstream>
#include <cstdlib>
#include <string>
using namespace std;

    string execCommand(const string& command) {
    string result;
    char buffer[128];
    FILE* pipe = popen(command.c_str(), "r");
    if (!pipe) {
        cerr << "Error: Failed to open pipe for command execution.\n";
        return "";
    }
    while (fgets(buffer, sizeof(buffer), pipe) != nullptr) {
        result += buffer;
    }
    pclose(pipe);
    
    // Remove trailing newline if present
    if (!result.empty() && result[result.size() - 1] == '\n') {
        result.pop_back();
    }
    return result;
}

int main(int argc, char* argv[]) {
    if (argc != 5) {
        cerr << "Usage: " << argv[0] << " <name> <T> <del_lammda> <number of iternations>\n";
        return 1;
    }

    string name = argv[1];
    string T = argv[2];
    string del_lammda = argv[3];
    string numIteration = argv[4];

    string commandF = "python fdti.py " + T + " " + del_lammda + " < " + name;
    string commandE = "python error.py " + T + " " + del_lammda + " " + numIteration + " < " + name;

    string F = execCommand(commandF);
    string e = execCommand(commandE);

    if (F.empty() || e.empty()) {
        cerr << "Error: One of the commands failed to execute.\n";
        return 1;
    }

    cout << F << " +/- " << e << endl;
    return 0;
}

