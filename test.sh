#python test script
echo "test 1: Wave File against Wave File"
python dan -f /course/cs4500f14/Assignments/A6/D1/bad0616.wav -f /course/cs4500f14/Assignments/A6/D1/z07.wav
echo " "
echo "test 2: Wave File against Directory"
python dan -f /course/cs4500f14/Assignments/A6/D1/sons2.wav -d /course/cs4500f14/Assignments/A6/D2/
echo " "
echo "test 3: Wave File against MP3 File"
python dan -f /course/cs4500f14/Assignments/A6/D4/Mpmm.wav -f /course/cs4500f14/Assignments/A6/D2/y01.mp3
echo " "
echo "test 4: MP3 File against Wave File"
python dan -f /course/cs4500f14/Assignments/A6/D1/janacek.mp3 -f /course/cs4500f14/Assignments/A6/D1/z03.wav
echo " "
echo "test 5: MP3 File against Directory"
python dan -f /course/cs4500f14/Assignments/A6/D1/rimsky.mp3 -d /course/cs4500f14/Assignments/A6/D2/
echo " "
echo "test 6: MP3 File against MP3 File"
python dan -f /course/cs4500f14/Assignments/A6/D1/rimsky.mp3 -f /course/cs4500f14/Assignments/A6/D2/y01.mp3
echo " "
echo "test 7: Directory against Directory"
python dan -d /course/cs4500f14/Assignments/A6/D2/ -d /course/cs4500f14/Assignments/A6/D4/
echo " "
echo "test 8: Directory against Wave File"
python dan -d /course/cs4500f14/Assignments/A6/D2/ -f /course/cs4500f14/Assignments/A6/D3/mMbm.wav
echo " "
echo "test 9: Directory against MP3 file"
python dan -d /course/cs4500f14/Assignments/A6/D5/ -f /course/cs4500f14/Assignments/A6/D2/y04.mp3



