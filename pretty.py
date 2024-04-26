import html
import tokenize
import keyword
import sys


def get_statistics(code):
    # Q1 Number of lines
    def num_of_line(filename):
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
            return len(lines)
        except Exception as e:
            print(f"Error occurred: {e}")
            return 0

    # Q2 Maximum line length
    def max_line_length(filename):
        try:
            with open(filename, 'r') as f:
                content = f.read()
            lines = content.splitlines()
            max_length = max(len(line) for line in lines)
            return max_length
        except Exception as e:
            print(f"Error occurred: {e}")
            return 0

    # Q3 Maximum variable length
    def max_variable_length(filename):
        max_var_length = 0
        try:
            with open(filename, 'rb') as f:
                tokens = tokenize.tokenize(f.readline)
                for token in tokens:
                    if token.type == tokenize.NAME and not keyword.iskeyword(token.string):
                        max_var_length = max(max_var_length, len(token.string))
            return max_var_length
        except Exception as e:
            print(f"Error occurred: {e}")
            return 0

    # Q4 Minimum variable length
    def min_variable_length(filename):
        variable_lengths = []
        try:
            with open(filename, 'rb') as f:
                tokens = tokenize.tokenize(f.readline)
                for token in tokens:
                    # Check if the token is a NAME and not a Python keyword
                    if token.type == tokenize.NAME and not keyword.iskeyword(token.string):
                        variable_lengths.append(len(token.string))
            return min(variable_lengths)
        except Exception as e:
            print(f"Error occurred: {e}")
            return 0

    # Q5 Number of comment lines
    def num_of_cl(filename):
        number_of_comment = 0
        try:
            with open(filename, 'rb') as f:
                tokens = tokenize.tokenize(f.readline)
                for token in tokens:
                    if token.type == tokenize.COMMENT:
                        number_of_comment += 1
            return number_of_comment
        except Exception as e:
            print(f"Error occurred: {e}")
            return 0

    # Q6 Number of definitions
    def num_of_def(filename):

        number_of_definitions = 0
        try:
            with open(filename, 'rb') as f:
                tokens = tokenize.tokenize(f.readline)
                for token in tokens:
                    if token.type == tokenize.NAME and token.string == 'def':
                        number_of_definitions += 1
            return number_of_definitions
        except Exception as e:
            print(f"Error occurred: {e}")
            return 0

    # Q7 Number of strings
    def num_of_str(filename):
        number_of_strings = 0
        try:
            with open(filename, 'rb') as f:
                tokens = tokenize.tokenize(f.readline)
                for token in tokens:
                    if token.type == tokenize.STRING:
                        number_of_strings += 1
            return number_of_strings
        except Exception as e:
            print(f"Error occurred: {e}")
            return 0

    # Q8 Number of numbers
    def num_of_num(filename):
        try:
            with open(filename, 'rb') as f:
                tokens = tokenize.tokenize(f.readline)
                number_of_numbers = 0
                for token in tokens:
                    if token.type == tokenize.NUMBER:
                        number_of_numbers += 1
            return number_of_numbers
        except Exception as e:
            print(f"Error occurred: {e}")
            return 0

    # Q9 Number of repeated constants
    def num_of_rc(filename):
        try:
            with open(filename, 'rb') as f:
                tokens = tokenize.tokenize(f.readline)
                repeat = {}
                for i in tokens:
                    if i.type in (tokenize.STRING, tokenize.NUMBER):
                        j = i.string
                        if j in repeat:
                            repeat[j] += 1
                        else:
                            repeat[j] = 1
                repeated_constants = 0
                for n in repeat.values():
                    if n > 1:
                        repeated_constants += 1
            return repeated_constants
        except Exception as e:
            print(f"Error occurred: {e}")
            return 0

    statistics = {
        'Number of lines = ': num_of_line(filename),
        'Maximum line length = ': max_line_length(filename),
        'Maximum variable length = ': max_variable_length(filename),
        'Minimum variable length = ': min_variable_length(filename),
        'Number of comment lines = ': num_of_cl(filename),
        'Number of definitions = ': num_of_def(filename),
        'Number of strings = ': num_of_str(filename),
        'Number of numbers = ': num_of_num(filename),
        'Number of repeated constants = ': num_of_rc(filename),

    }

    return statistics


def format_code_for_html(filename):
    with (open(filename, 'r') as file):
        # We creat a code_book, so if after the tokenize(), the missing item can be found here
        code_book = {}
        original_code = file.readlines()
        line_no = 1
        for line in original_code:
            code_book[line_no] = line
            line_no += 1
        file.seek(0)

        last_pos = (0, 0)  # start with 0 to ensure the first token position will be larger than it
        new_line = ''  # create an empty string to store the coding with class added
        add_missing = 0
        space_need = 0
        for token in tokenize.generate_tokens(file.readline):
            # print(token) # for test purpose only, print all the token
            # print(token.type) # for test purpose only, print all the token type
            # print(token.line) # for test purpose only, print all the token line
            if token.start[0] > last_pos[0] + 1:  # check if there is a line missing after tokenize()
                currect_check_line = last_pos[0] + 1
                while currect_check_line < token.start[0]:
                    new_line += code_book[currect_check_line]  # find the missing item from code_book
                    currect_check_line += 1
                last_pos = (token.start[0], 0)
            elif token.start[0] == last_pos[0] + 1 or multi_line:  # check if starting a newline
                if add_missing == 1:
                    new_line += ' ' * space_need + '\\\n'
                multi_line = False
                last_pos = (token.start[0], 0)
                # check if there is a \\\n in original line
                if token.line.endswith('\\\n'):
                    add_missing = 1
                else:
                    add_missing = 0
            # Add back the missing white space after tokenize
            new_line += ' ' * (token.start[1] - last_pos[1])
            # check token.type by token.type number, sometimes two different number is referring to same type.
            if token.type == tokenize.STRING:
                if token.start[0] == token.end[0]:
                    new_line += '<span class="string">' + html.escape(token.string) + '</span>'
                else:
                    # since this string span multiple lines, we have to add the span/class for each line
                    for lines in token.string.splitlines():
                        new_line += '<span class="string">' + html.escape(lines) + '</span>\n'
                    # there is an additional \n added at the end of this token, just remove it
                    new_line = new_line[:-1]
            elif token.type == tokenize.OP:
                new_line += '<span class="operator">' + html.escape(token.string) + '</span>'
            elif token.type == tokenize.COMMENT:
                new_line += '<span class="comment">' + html.escape(token.string) + '</span>'
                add_missing = 0  # In comment, the \\\n will not miss
            elif token.type == tokenize.NUMBER:
                new_line += '<span class="number">' + html.escape(token.string) + '</span>'
            elif keyword.iskeyword(token.string):
                new_line += '<span class="keyword">' + html.escape(token.string) + '</span>'
            elif token.type == tokenize.NAME:
                new_line += '<span class="variable">' + html.escape(token.string) + '</span>'
            elif token.type == tokenize.NL or token.type == tokenize.NEWLINE:
                new_line += '\n'
            else:
                new_line += token.string
            if add_missing == 1:
                # calculate the space needed before adding \\\n at the end
                #using the original line length - last token column - \\\n it self 2 position
                space_need = len(code_book[token.end[0]]) - token.end[1] -2
            last_pos = token.end
            if token.end[0] > token.start[0]:
                multi_line = True

    # The process to add the line number
    final_code = ''
    i = 1
    for line in new_line.splitlines():
        # add line-number and replace \n with <br> in HTML language
        line = '<span class="line{}">'.format(i) + str(i) + '</span>' + ' ' * (10 - len(str(i))) + line
        i += 1
        final_code += '<br>' + line
    # Add at the end to allow jump to end
    final_code += '<span id="end"></span>'

    return "<pre><code>" + final_code + "</code></pre>"


def fill_html_template(stats, formatted_code):
    statistics_html = "<ul>"
    for key, value in stats.items():
        statistics_html += "<li>" + str(key) + str(value) + "</li>"
    statistics_html += "</ul>"

    html_content = """
    <!doctype html>
    <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>Pretty Python</title>
            <style>
                pre {{font-size: 16pt}}
                .variable {{color: black}}
                .comment {{color: green}}
                .keyword {{color: blue}}
                .string {{color: orange}}
                .number {{color: red}}
                .operator {{color: purple}}
            </style>
        </head>
        <body>
            <h1>Python code inspector</h1>
            <span>Current Date and time </span>
            <div id="datetime">
                <script>
                    setInterval("document.getElementById('datetime').innerHTML=new Date().toLocaleString();", 500);
                </script>
            </div>
            <ul>
                <li><a href="#stats">Statistics</a></li>
                <li><a href="#code">Code</a></li>
                <li><a href="#end">End</a></li>
            </ul>
            <div id="stats">
                <h2>Statistics</h2>
                {statistics_html}
            </div>
            <div id="code">
                <h2>Python code</h2>
                {formatted_code}
            </div>
        </body>
    </html>
    """.format(statistics_html=statistics_html, formatted_code=formatted_code)

    return html_content


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 your_script.py <input_file>')
        sys.exit(1)

    try:
        filename = sys.argv[1]
        with open(filename, 'r') as file:
            if not filename.lower().endswith('.py'):
                print('The file is not a Python file')
                sys.exit(1)
            code = file.read()
        stats = get_statistics(code)
        line = str(stats['Number of lines = '])
        formatted_code = format_code_for_html(filename)
        full_html = fill_html_template(stats, formatted_code)
        sys.stdout.write(full_html)
        sys.stdout.close()
    except FileNotFoundError:
        print('Error: Can not find this file, please try another file.')
        sys.exit(1)
    except Exception:
        print('Ops, something goes wrong')
        sys.exit(1)
