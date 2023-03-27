def replace_quotes(html_code):
    return html_code.replace('"', "'")

html_code = input("Enter HTML code: ")
new_html_code = replace_quotes(html_code)

with open("output.html", "w") as f:
    f.write(new_html_code)

print("HTML code saved to output.html")
