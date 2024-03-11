from flask import Flask, render_template, request
import csv
import os
import re
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Function to count occurrences of a word in a text file
def count_word_occurrences(file_path, word):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        # Using regular expression to find word occurrences (case insensitive)
        occurrences = len(re.findall(r'\b{}\b'.format(word), text, flags=re.IGNORECASE))
        return occurrences

# Function to parse CSV file and calculate word frequency for each year
def calculate_word_frequency(csv_file, folder_path, word):
    # Dictionary to store word frequencies for each year
    word_frequency_by_year = {}

    with open(csv_file, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        # next(csv_reader)  # Skip header row if present
        for row in csv_reader:
            # print(row)
            file_name, date = row
            year = date.split('-')[2]  # Extract year from date
            file_path = os.path.join(folder_path, file_name)
            file_path += '.txt'
            if os.path.exists(file_path):
                occurrences = count_word_occurrences(file_path, word)
                if year in word_frequency_by_year:
                    word_frequency_by_year[year] += occurrences
                else:
                    word_frequency_by_year[year] = occurrences

    return word_frequency_by_year

def sortDictionary(dictionary):
    myKeys = list(dictionary.keys())
    myKeys.sort()
    sorted_dict = {i: dictionary[i] for i in myKeys}
    return sorted_dict

def compute_frequency_dict(word, csv_file, folder_path):
    # Calculate word frequency
    freq_dictionary = calculate_word_frequency(csv_file, folder_path, word)

    sorted_dict = sortDictionary(freq_dictionary)
    
    return sorted_dict

# This functions plots Ngram with legend outside the graph
def plot_nGram(words):
    # csv_file = 'Book1.csv'
    # folder_path = 'F:\\IDP\\ngramViewer\\version4\\Book1'

    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(current_dir, 'Book1.csv')
    folder_path = os.path.join(current_dir, 'Book1')

    lst = []
    for i in range(len(words)):
        dict1 = compute_frequency_dict(words[i], csv_file, folder_path)
        xvalues = list(dict1.keys())
        yvalues = list(dict1.values())
        lst.append([xvalues, yvalues])

    # Plotting the line chart
    for i in range(len(words)):
        plt.plot(lst[i][0], lst[i][1], marker='o', label=words[i])

    plt.xlabel('Year')
    plt.ylabel('Frequency')
    plt.title('Frequency of Words in collected works of Mahatma Gandhi')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.grid(True)
    plt.tight_layout()

    # Move the legend outside the plot
    plt.legend(loc='center left', bbox_to_anchor=(1.05, 1))
    
   # Save the plot to a BytesIO object
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', bbox_inches='tight')  # Add bbox_inches='tight'
    img_buffer.seek(0)
    plot_data = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    plt.close()  # Close the plot to prevent displaying it directly in Flask
    
    
    return plot_data

# This functions plots Ngram with legend within the graph
# def plot_nGram(words):
#     csv_file = 'Book1.csv'
#     folder_path = 'F:\\IDP\\ngramViewer\\version4\\Book1'
#     lst = []
#     for i in range(len(words)):
#         dict1 = compute_frequency_dict(words[i], csv_file, folder_path)
#         xvalues = list(dict1.keys())
#         yvalues = list(dict1.values())
#         lst.append([xvalues, yvalues])

#     # Plotting the line chart
#     for i in range(len(words)):
#         plt.plot(lst[i][0], lst[i][1], marker='o', label=words[i])


#     plt.xlabel('Year')
#     plt.ylabel('Frequency')
#     plt.title('Frequency of Words in collected works of Mahatma Gandhi')
#     plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
#     plt.legend()
#     plt.grid(True)
#     plt.tight_layout()

#     # Save the plot to a BytesIO object
#     img_buffer = BytesIO()
#     plt.savefig(img_buffer, format='png')
#     img_buffer.seek(0)
#     plot_data = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
#     plt.close()  # Close the plot to prevent displaying it directly in Flask
    
#     return plot_data


# Define route for web app
@app.route('/', methods=['GET', 'POST'])
def index(): 
    plot_data = None
    if request.method == 'POST':
        words = request.form.get('words')
        words = words.split(',')  # Split input by comma to get individual words
        plot_data = plot_nGram(words)
    return render_template('index.html', plot_data=plot_data)

if __name__ == '__main__':
    app.run(debug=True)


# from flask import Flask, render_template, request
# import csv
# import os
# import re
# import matplotlib.pyplot as plt
# from io import BytesIO
# import base64

# app = Flask(__name__)

# # Function to count occurrences of a word in a text file
# def count_word_occurrences(file_path, word):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         text = file.read()
#         # Using regular expression to find word occurrences (case insensitive)
#         occurrences = len(re.findall(r'\b{}\b'.format(word), text, flags=re.IGNORECASE))
#         return occurrences

# # Function to parse CSV file and calculate word frequency for each year
# def calculate_word_frequency(csv_file, folder_path, word):
#     # Dictionary to store word frequencies for each year
#     word_frequency_by_year = {}

#     with open(csv_file, 'r') as csvfile:
#         csv_reader = csv.reader(csvfile)
#         # next(csv_reader)  # Skip header row if present
#         for row in csv_reader:
#             # print(row)
#             file_name, date = row
#             year = date.split('-')[2]  # Extract year from date
#             file_path = os.path.join(folder_path, file_name)
#             file_path += '.txt'
#             if os.path.exists(file_path):
#                 occurrences = count_word_occurrences(file_path, word)
#                 if year in word_frequency_by_year:
#                     word_frequency_by_year[year] += occurrences
#                 else:
#                     word_frequency_by_year[year] = occurrences

#     return word_frequency_by_year

# def sortDictionary(dictionary):
#     myKeys = list(dictionary.keys())
#     myKeys.sort()
#     sorted_dict = {i: dictionary[i] for i in myKeys}
#     return sorted_dict

# def compute_frequency_dict(word, csv_file, folder_path):
#     # Calculate word frequency
#     freq_dictionary = calculate_word_frequency(csv_file, folder_path, word)

#     sorted_dict = sortDictionary(freq_dictionary)
    
#     return sorted_dict

# def plot_nGram(words):
#     csv_file = 'Book1.csv'
#     folder_path = 'F:\\IDP\\ngramViewer\\version4\\Book1'
#     lst = []
#     for i in range(len(words)):
#         dict1 = compute_frequency_dict(words[i], csv_file, folder_path)
#         xvalues = list(dict1.keys())
#         yvalues = list(dict1.values())
#         lst.append([xvalues, yvalues])

#     # Plotting the line chart
#     for i in range(len(words)):
#         plt.plot(lst[i][0], lst[i][1], marker='o', label=words[i])


#     plt.xlabel('Year')
#     plt.ylabel('Frequency')
#     plt.title('Frequency of Words in collected works of Mahatma Gandhi')
#     plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
#     plt.legend()
#     plt.grid(True)
#     plt.tight_layout()

#     # Save the plot to a BytesIO object
#     img_buffer = BytesIO()
#     plt.savefig(img_buffer, format='png')
#     img_buffer.seek(0)
#     plot_data = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
#     plt.close()  # Close the plot to prevent displaying it directly in Flask
    
#     return plot_data

# # Define route for web app
# @app.route('/', methods=['GET', 'POST'])
# def index(): 
#     if request.method == 'POST':
#         words = request.form.get('words')
#         words = words.split(',')  # Split input by comma to get individual words
#     else:
#         words = ['freedom', 'peace']  # Default words for demonstration
    
#     plot_data = plot_nGram(words)
#     return render_template('index.html', plot_data=plot_data)

# if __name__ == '__main__':
#     app.run(debug=True)

