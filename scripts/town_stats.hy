(import [json [dumps]])
(import [os [listdir]])
(import [os.path [getmtime]])
(import [datetime [datetime]])

(import [sh [find facter]])

;; this script emits json on standard out that has information about tilde.town
;; users. It denotes who has not updated their page from the default. It also
;; reports the time this script was run. The user list is sorted by public_html update time.

(defn slurp [filename]
  (try
    (.read (apply open [filename "r"] {"encoding" "utf-8"}))
  (catch [e Exception]
    "")))

(def default-html (slurp "/etc/skel/public_html/index.html"))

(defn default? [username]
  (= default-html (slurp (.format "/home/{}/public_html/index.html" username))))

(defn bounded-find [path]
  ;; find might return 1 but still have worked fine (because of dirs it can't
  ;; go into)
  (apply find [path "-maxdepth" "3"] {"_ok_code" [0 1]}))

(defn guarded-mtime [filename]
  (let [[path (.rstrip filename)]]
    (try
      (getmtime path)
    (catch [e Exception]
      0))))

(defn modify-time [username]
  (->> (.format "/home/{}/public_html" username)
       bounded-find
       (map guarded-mtime)
       list
       max))

(defn sort-user-list [usernames]
  (apply sorted [usernames] {"key" modify-time}))

(defn user-generator [] (->> (listdir "/home")
                             (filter (fn [f] (and (not (= f "ubuntu")) (not (= f "poetry")))))))

(if (= __name__ "__main__")
  (let [[all_users (->> (user-generator)
                        sort-user-list
                        reversed
                        (map (fn [un] {"username" un
                                       "default" (default? un)}))
                        list)
         [live_users (-> (filter (fn [u] (not (get u "default"))) all_users)
                         list)]]
        [data {"all_users" users
               "live_users" live_users
               "active_user_count" (-> (. (facter "active_user_count") stdout)
                                       .strip
                                       int)
               "generated_at" (.strftime (.now datetime) "%Y-%m-%d %H:%M:%S")
               "num_users" (len users)}]]
    (print (dumps data))))
