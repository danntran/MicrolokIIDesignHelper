# --------------------------- #
# --- Function Definitons --- #
# --------------------------- #


def column_create(input_arr, col_num):
	# Create array of arrays based off column number
	col_arr = []
	for i in range(0,col_num,1):
		val_arr = input_arr[i::col_num]
		col_arr.append(val_arr)
	return col_arr

def array_combine(col_exist, col_adjoin):
	# Combine existing text column with column to append
	output_array = []							# Create empty output array to store combined column array
	max_str_len = len(max(col_exist, key=len))	# Determine number of characters within the largest string of existing column
	max_empty_str_len = max_str_len + 4			# Add single tab (4 whitespaces) to maximum length

	# Check length of existing and adjoining column entries
	last_val=""
	if len(col_exist) != len(col_adjoin):
		last_val = col_exist[-1]
		col_exist.pop()

	# Loop through each entry in existing column, adding appropriate whitespace 
	# between each entry of existing and adjoining column and appending result to output array
	for i, val in enumerate(col_exist):
		whitespace_len = max_empty_str_len - len(val)
		str_combine = col_exist[i] + " " * whitespace_len + col_adjoin[i]
		output_array.append(str_combine)

	# Add last entry to output array, if it exists
	if last_val:
		output_array.append(last_val)

	return output_array	# return output array

def add_empty_rows(text_arr):
	# Add an empty row to text array, every block of 4
	spacepos = range(4,len(text_arr),4)
	for j in reversed(spacepos):
		text_arr.insert(j, "")
	return text_arr

def addcomma2txt(text):
	# adds commas to the end of each row
	output_txt = []
	if text:
		for bit in text[:-1]:
			output_txt.append(bit+",")
		output_txt.append(text[-1]+";")
	return output_txt



def column_divide(input_array, num_col, rmcomma):
	# Create output text array based off input text and number of columns to segment
	output_text_array = [] # Create empty output array for text file

	if input_array: # check if empty array
		if not rmcomma: # check if user wants commas
			bits_arr = addcomma2txt(input_array)
		else:
			bits_arr = input_array
		
		column_array = column_create(bits_arr, num_col)	# Create array of text column arrays

		if num_col == 1:
			output_text_array = bits_arr
			
		elif num_col == 2:
			column_text_combine = array_combine(column_array[0],column_array[1])
			output_text_array = add_empty_rows(column_text_combine)

		elif (3 <= num_col <= 8):
			column_text_combine = array_combine(column_array[0],column_array[1])
			k=2
			while k < num_col:
				column_text_combine = array_combine(column_text_combine,column_array[k])
				k += 1
			output_text_array = add_empty_rows(column_text_combine)

	return output_text_array	# return output text array

def formattxt(text, ncols, rmcomma):
	# Get text and format them appropriately
	bits = column_divide(text, ncols, rmcomma)
	output = "\n".join(bits)
	return output

if __name__ == '__main__':
	# Open the file called "inputbits.txt" and store the text into
	# an array called input_array.
	input_txt = open('inputbits.txt','r')
	input_txt_array = input_txt.read().splitlines()
	input_txt.close()

	# Convert the input_array to its desired tabular layout
	output = column_divide(input_txt_array, 3, 0)

	# Write output array to file called "outputfile.txt"
	with open("outputfile.txt", "w") as outfile:
		outfile.write("\n".join(output))