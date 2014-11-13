#python error testing script
echo "Test 1: Providing invalid file path"
python dan -f /course/cs4500f14/Assignments/A6/D2/sdf.wav -d /course/cs4500f14/Assignments/A6/D6
echo " "
echo "Test 2: Providing only files without options"
python dan /course/cs4500f14/Assignments/A6/D1/bad0616.wav /course/cs4500f14/Assignments/A6/D1/z03.wav
echo " "
echo "Test 3: Providing only 1 file"
python dan -f /course/cs4500f14/Assignments/A6/D1/z07.wav
echo " "
echo "Test 4: Providing incorrect options"
python dan -f /course/cs4500f14/Assignments/A6/D2/ -d /course/cs4500f14/Assignments/A6/D1/sons2.wav
echo "Tes 5: Providing unsupported file format"
python dan -f /course/cs4500f14/Assignments/A6/D1/z07.txt -f /course/cs4500f14/Assignments/A6/README 
