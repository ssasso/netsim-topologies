#!/bin/bash

echo "Initializing codespace $CODESPACE_NAME..."

gh codespace ports visibility 5001:public -c $CODESPACE_NAME

echo "All set. Good luck! :)"
