/*
Лабораторная работа №1
Выполнил студент 321702 группы
Пшенов Евгений Витальевич
Вариант 2 : проверить является ли формула сокращенного языка логики высказываний общезначимой (тавтологией)
Исполняемый файл программы
10.05.2025
Источники:
-Учебно-методическое пособие по ЛОИС

(A/\(B/\(C/\D)))
(A\/(1\/(B\/1)))
(A/\(B->(C~(D\/E))))
(A\/(B/\(C~(D/\(E\/(!F/\(G/\(H\/(I->(J/\(K/\(L/\(M~(N->(O\/(P/\(Q~(R/\(S/\(T->(U\/(V\/(W/\(X/\(Y->Z)))))))))))))))))))))))))
(1\/(A\/(B\/(C\/(D\/(E\/(F/\(G/\(H/\(I/\(J/\(K/\(L/\(M/\(N\/(O\/(P\/(Q\/(R\/(A/\(B/\(C/\(D/\(E/\(F/\(G/\(H/\(I/\(J/\(K/\(L/\(M/\(N/\(O/\(P/\(Q/\(R/\(S))))))))))))))))))))))))))))))))))))))
(1\/(A/\(B/\(C/\(D/\(E/\(F/\(G/\(H/\(I/\(J/\(K/\(L/\(M/\(N/\(O/\(P/\(Q/\(R/\(S/\(T/\(U/\(V/\(W/\(X/\(Y/\Z))))))))))))))))))))))))))
*/
#include <iostream>
#include <string>
#include <stack>
#include <vector>
#include <chrono> 
using namespace std;
using namespace std::chrono;

const char OPEN_BRACKET = '(';
const char CLOSE_BRACKET = ')';
const char AND = '&';
const char OR = '|';
const char IMPLIES = '<';
const char EQUIVALENT = '~';
const char NEGATION = '!';

const vector<char> VARS = { 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z' };
const vector<char> CONSTS = { '0', '1' };
const vector<char> BINARY_OPS = { AND, OR, IMPLIES, EQUIVALENT };
const vector<char> VALID_CHARS = {
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    '0', '1', AND, OR, IMPLIES, EQUIVALENT, NEGATION, OPEN_BRACKET, CLOSE_BRACKET
};

enum SymbolType {
    VARIABLE,
    CONSTANT,
    BINARY_OPERATOR,
    UNARY_OPERATOR,
    BRACKET_OPEN,
    BRACKET_CLOSE
};

struct Token {
    string value;
    SymbolType type;
};

int get_priority(char operation) {
    switch (operation) {
    case '(':
        return 1;
    case '<':
        return 3;
    case '~':
        return 3;
    case '&':
        return 5;
    case '|':
        return 4;
    default:
        return 0;
    }
}

void testing_mode() {
    struct TestCase {
        string formula;
        bool isTautology;
        string explanation;
    };

    vector<TestCase> testCases = {
        {"(A/\\B)", false, "Формула (A/\\B) зависит от значений A и B, при A=0, B=1 она равна 0."},
        {"(A->(B\\/C))", false, "Формула (A->(B\\/C)) не всегда истинна, например, при A=1, B=0, C=0 она равна 0."},
        {"A", false, "Переменная A не является тавтологией, так как её значение может быть 0."},
        {"(A\\/1)", true, "Формула (A\\/1) всегда истинна, так как константа 1 делает дизъюнкцию истинной."},
        {"(!((A\\/(B\\/C))\\/(!A)))", true, "Формула всегда истинна."}
    };

    cout << "Для каждой формулы определите, является ли она общезначимой." << endl;

    for (size_t i = 0; i < testCases.size(); i++) {
        const TestCase& test = testCases[i];
        cout << test.formula << endl;
        cout << "Является ли она тавтологией? (1 - является, 2 - не является): ";

        string answer;
        getline(cin, answer);

        bool userAnswer;
        if (answer == "1")
            userAnswer = true;
        else if (answer == "2")
            userAnswer = false;
        else {
            cout << "Введите 1 или 2." << endl;
            i--;
            continue;
        }

        if (userAnswer == test.isTautology) {
            cout << "Верно" << endl;
        }
        else {
            cout << "Не верно" << endl;
            cout << test.explanation << endl;
        }
    }
}

SymbolType IdentifySymbol(char c) {
    if (c >= 'A' && c <= 'Z') return VARIABLE;
    if (c == '0' || c == '1') return CONSTANT;
    if (c == AND || c == OR || c == IMPLIES || c == EQUIVALENT) return BINARY_OPERATOR;
    if (c == NEGATION) return UNARY_OPERATOR;
    if (c == OPEN_BRACKET) return BRACKET_OPEN;
    return BRACKET_CLOSE;
}

string preprocessing(const string& formula) {
    string result = "";
    for (size_t i = 0; i < formula.length(); i++) {
        if (formula[i] != ' ' && formula[i] != '\t') {
            result += formula[i];
        }
    }

    string final_result = "";
    for (size_t i = 0; i < result.length(); i++) {
        if (result[i] == '-') {
            if (i + 1 < result.length() && result[i + 1] == '>') {
                final_result += '<';
                i++;
            }
            else {
                final_result += result[i];
            }
        }
        else if (result[i] == '/') {
            if (i + 1 < result.length() && result[i + 1] == '\\') {
                final_result += '&';
                i++;
            }
            else {
                final_result += result[i];
            }
        }
        else if (result[i] == '\\') {
            if (i + 1 < result.length() && result[i + 1] == '/') {
                final_result += '|';
                i++;
            }
            else {
                final_result += result[i];
            }
        }
        else {
            final_result += result[i];
        }
    }
    return final_result;
}

bool is_correct(string& formula) {
    if (formula.empty())
        return false;

    int bracket_count = 0;
    for (char c : formula) {
        bool valid_char = false;
        for (char valid : VALID_CHARS) {
            if (c == valid) {
                valid_char = true;
                break;
            }
        }
        if (!valid_char)
            return false;

        if (c == OPEN_BRACKET)
            bracket_count++;
        else if (c == CLOSE_BRACKET)
            bracket_count--;
        if (bracket_count < 0)
            return false;
    }
    return bracket_count == 0;
}

vector<Token> tokenize(const string& input) {
    vector<Token> tokens;
    for (size_t i = 0; i < input.length(); i++) {
        if (input[i] == ' ' || input[i] == '\t') {
            continue;
        }

        if (input[i] == '!') {
            string value = string(1, input[i]);
            tokens.push_back({ value, UNARY_OPERATOR });
            continue;
        }

        if (input[i] == '&' || input[i] == '|' || input[i] == '<' || input[i] == '~') {
            string value = string(1, input[i]);
            tokens.push_back({ value, BINARY_OPERATOR });
            continue;
        }

        if (input[i] == '(') {
            string value = string(1, input[i]);
            tokens.push_back({ value, BRACKET_OPEN });
            continue;
        }

        if (input[i] == ')') {
            string value = string(1, input[i]);
            tokens.push_back({ value, BRACKET_CLOSE });
            continue;
        }

        if (isalpha(input[i])) {
            string var = string(1, input[i]);
            tokens.push_back({ var, VARIABLE });
            continue;
        }

        if (isdigit(input[i])) {
            string const_val = string(1, input[i]);
            tokens.push_back({ const_val, CONSTANT });
            continue;
        }
    }
    return tokens;
}


string method(string& formula, int depth, bool check) {
    string processed = preprocessing(formula);
    if (processed.empty() || !is_correct(processed)) {
        if (check) cout << "Ошибка: некорректная формула или пустой ввод." << endl;
        return "";
    }

    vector<Token> operatorStack;
    int negationCount = 0;
    vector<Token> tokens = tokenize(processed);
    string output;

    for (int i = 0; i < tokens.size(); i++) {
        const Token& current = tokens[i];
        if (current.type == VARIABLE || current.type == CONSTANT) {
            output += current.value;
            for (int n = 0; n < negationCount; n++) {
                output += NEGATION;
            }
            negationCount = 0;
        }
        else if (current.type == UNARY_OPERATOR) {
            negationCount++;
        }
        else if (current.type == BRACKET_OPEN) {
            operatorStack.push_back(current);
            depth++;
        }
        else if (current.type == BRACKET_CLOSE) {
            while (!operatorStack.empty() && operatorStack.back().type != BRACKET_OPEN) {
                output += operatorStack.back().value;
                operatorStack.pop_back();
            }
            if (!operatorStack.empty()) operatorStack.pop_back();
            depth--;
            for (int n = 0; n < negationCount; n++) {
                output += NEGATION;
            }
            negationCount = 0;
        }
        else if (current.type == BINARY_OPERATOR) {
            while (!operatorStack.empty() && operatorStack.back().type != BRACKET_OPEN && get_priority(current.value[0]) <= get_priority(operatorStack.back().value[0])) {
                output += operatorStack.back().value;
                operatorStack.pop_back();
            }
            operatorStack.push_back(current);
        }
    }

    while (!operatorStack.empty()) {
        if (operatorStack.back().type == BRACKET_OPEN || operatorStack.back().type == BRACKET_CLOSE) {
            if (check) cout << "Ошибка: несбалансированные скобки." << endl;
            return "";
        }
        output += operatorStack.back().value;
        operatorStack.pop_back();
    }

    for (int n = 0; n < negationCount; n++) {
        output += NEGATION;
    }
    return output;
}

int EvalFormula(const string& notation, const vector<char>& variables, const vector<int>& values) {
    vector<int> evalStack;
    for (char token : notation) {
        switch (IdentifySymbol(token)) {
        case VARIABLE: {
            int value = 0;
            for (int i = 0; i < variables.size(); i++) {
                if (variables[i] == token) {
                    value = values[i];
                    break;
                }
            }
            evalStack.push_back(value);
            break;
        }
        case CONSTANT: {
            int value = token - '0';
            evalStack.push_back(value);
            break;
        }
        case UNARY_OPERATOR: {
            int val = evalStack.back();
            evalStack.pop_back();
            evalStack.push_back(1 - val);
            break;
        }
        case BINARY_OPERATOR: {
            int b = evalStack.back();
            evalStack.pop_back();
            int a = evalStack.back();
            evalStack.pop_back();
            int res = 0;
            if (token == AND) {
                res = a & b;
            }
            else if (token == OR) {
                res = a | b;
            }
            else if (token == EQUIVALENT) {
                if (a == b) {
                    res = 1;
                }
                else {
                    res = 0;
                }
            }
            else {
                if (!a || b) {
                    res = 1;
                }
                else {
                    res = 0;
                }
            }
            evalStack.push_back(res);
            break;
        }
        default:
            break;
        }
    }
    return evalStack.back();
}

bool is_tautology(const string& notation, int maxVars, bool verbose) {
    vector<char> vars;
    for (char c : notation) {
        if (IdentifySymbol(c) == VARIABLE) {
            bool exists = false;
            for (char v : vars) {
                if (v == c) {
                    exists = true;
                    break;
                }
            }
            if (!exists) vars.push_back(c);
        }
    }

    if (vars.empty()) {
        vector<char> emptyVars;
        vector<int> emptyVals;
        return EvalFormula(notation, emptyVars, emptyVals) == 1;
    }

    if (vars.size() > static_cast<size_t>(maxVars)) {
        if (verbose) cout << "Ошибка: превышено максимальное число переменных (" << maxVars << ")." << endl;
        return false;
    }

    size_t num_combinations = static_cast<size_t>(std::pow(2, vars.size()));
    for (size_t i = 0; i < num_combinations; i++) {
        vector<int> var_values(vars.size());
        for (size_t j = 0; j < vars.size(); j++) {
            int bit_value = (i >> (vars.size() - 1 - j)) & 1;
            var_values[j] = bit_value;
        }
        int result = EvalFormula(notation, vars, var_values);
        if (result != 1) {
            if (verbose) {
                cout << "Формула не является общезначимой.\n\n\n";
                cout << "Пример: ";
                for (size_t k = 0; k < vars.size(); k++) {
                    cout << vars[k] << "=" << var_values[k] << " ";
                }
                cout << "-> " << result << endl;
            }
            return false;
        }
    }
    if (verbose) cout << "Формула является общезначимой.\n\n\n";
    return true;
}

bool is_isolated(const string& input, int& i) {
    size_t openBracket = input.find('(');
    while (openBracket != string::npos) {
        size_t closeBracket = input.find(')', openBracket);
        if (closeBracket != string::npos) {
            string inside = input.substr(openBracket + 1, closeBracket - openBracket - 1);
            if (inside.length() == 1 && isupper(inside[0]) && inside[0] != '0' && inside[0] != '1') {
                cout << "Ошибка: переменная в скобках без действий." << endl;
                i--;
                return true;
            }
        }
        openBracket = input.find('(', openBracket + 1);
    }

    string processed = preprocessing(input);
    vector<Token> tokens = tokenize(processed);
    stack<size_t> bracketStack;
    for (size_t j = 0; j < tokens.size(); j++) {
        if (tokens[j].type == BRACKET_OPEN) {
            bracketStack.push(j);
        }
        else if (tokens[j].type == BRACKET_CLOSE) {
            if (!bracketStack.empty()) {
                bracketStack.pop();
            }
        }
        else if (tokens[j].type == BINARY_OPERATOR) {
            if (bracketStack.empty()) {
                cout << "Ошибка: операция " << tokens[j].value << " должна быть в скобках, например (A\\/B)." << endl;
                i--;
                return true;
            }
            bool hasLeftOperand = false;
            bool hasRightOperand = false;

            for (int k = static_cast<int>(j) - 1; k >= 0; k--) {
                if (tokens[k].type == BRACKET_OPEN) {
                    break;
                }
                if (tokens[k].type == VARIABLE || tokens[k].type == CONSTANT) {
                    hasLeftOperand = true;
                    break;
                }
            }

            for (size_t k = j + 1; k < tokens.size(); k++) {
                if (tokens[k].type == BRACKET_CLOSE) {
                    break;
                }
                if (tokens[k].type == VARIABLE || tokens[k].type == CONSTANT) {
                    hasRightOperand = true;
                    break;
                }
            }

            if (!hasLeftOperand || !hasRightOperand) {
                cout << "Ошибка: операция " << tokens[j].value << " не имеет двух операндов." << endl;
                i--;
                return true;
            }
        }
    }

    if (!bracketStack.empty()) {
        cout << "Ошибка: несбалансированные скобки." << endl;
        i--;
        return true;
    }

    return false;
}

int main() {
    setlocale(LC_ALL, "RU");

    string choice;
    while (true) {
        cout << "Выберите режим:" << endl;
        cout << "1. Тестовый режим" << endl;
        cout << "2. Ввод формул вручную" << endl;
        cout << "3. Выход" << endl;

        getline(cin, choice);

        if (choice == "1") {
            testing_mode();
        }

        else if (choice == "2") {
            for (int i = 0; i < 3; i++) {
                cout << "Справка по логическим операциям:" << endl;
                cout << "Или: \\/" << endl;
                cout << "И: /\\" << endl;
                cout << "Отрицание: !" << endl;
                cout << "Импликация: ->" << endl;
                cout << "Эквиваленция: ~" << endl;
                cout << "Введите логическую формулу:" << endl;

                string input;
                getline(cin, input);

                if (input.empty()) {
                    cout << "Ошибка: пустая строка" << endl;
                    i--;
                    continue;
                }
                //auto start = high_resolution_clock::now();
                string notation = method(input, 100, false);
                if (notation.empty()) {
                    cout << "Ошибка: некорректная формула" << endl;
                    continue;
                }

                if (!is_isolated(input, i)) {
                    bool check = is_tautology(notation, 100, true);
                }
                //auto end = high_resolution_clock::now();
                //auto duration = duration_cast<seconds>(end - start);
                //cout << "Время вычисления: " << duration.count() << " с" << endl;
            }
        }
        else if (choice == "3") {
            break;
        }
        else {
            cout << "Некорректный ввод\n";
        }
    }

    return 0;
}
