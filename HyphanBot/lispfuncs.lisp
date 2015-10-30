(load 'prelisp)

(defun test()
    (format t "~a~%" "This is a test..")
(values))

(defun hyphan(&optional arg1)
	(if (eq arg1 nil)
		(format t "Yes? What do you need?")
		(format t arg1))
(values))

(defun heart(&optional arg1 face)
	(if (eq arg1 nil)
		(format t "Who or what do you want me to heart?")
		(if (eq face t)
			(format t (concatenate 'string "😍 " arg1))
			(format t (concatenate 'string "❤ " arg1))))
(values))

(defun directory(&optional path)
	(format t "Fuck you.")
(values))

(defun prelisp()
	(with-open-file (stream "prelisp")
		(do ((line (read-line stream nil) (read-line stream nil))) ((null line)) 
		(write-line line)))
(values))

(defun vaal()
	(dotimes (i 5) (format t "Vaal is shit~&"))
(values))

(defun exit()
	(format t "I shall not take the commands of an inferior race.")
(values))

(defun quit()
	(format t "Hyphan never quits, even if you tell 'er to.")
(values))
