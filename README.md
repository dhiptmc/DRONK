# DRONK - Drink delivery with drone and mobile application based on database system
本專題規劃DRONK系統架構分為前端（客戶端）、後端（資料庫工作人員）及無人機三大部分。  
前端（客戶端）使用手機App下單選購飲料，將訂單內容上傳至雲端資料庫。後端（資料庫工作人員）設置飲料菜單資訊，並管理訂單。於接收到新訂單時對無人機提出需求，執行任務檔dronk.py。  
無人機透過遠端遙控的樹莓派啟動，樹莓派藉由機載4G行動網路從後台更新訂單資料，記錄下新訂單的客戶資訊及客戶指定之目的地。無人機飛往目的地遞交飲料後返航基地。
