;;; install.el --- Install blender addon to engine addons directory


;;; Commentary:
;;

;;; Code:

(progn
  (delete-directory "e:/bottleship/code/tk-blender/resources/scripts/addons/btl_blender_exportgroups/"
                    t)
  (copy-directory "e:/bottleship/code/btl_blender_exportgroups/"
                  "e:/bottleship/code/tk-blender/resources/scripts/addons/btl_blender_exportgroups"))

;;; install.el ends here
