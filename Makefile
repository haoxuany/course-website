
updateall:
	cd generation && ./push.py && \
		cd ../site && git add . && \
		git commit -m "Snapshot of `date`" && git push -f
