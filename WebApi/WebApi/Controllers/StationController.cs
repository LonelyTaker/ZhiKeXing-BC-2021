using System;
using System.Linq;
using System.Web.Http;
using System.Web.Http.Cors;
using MySql.Data.MySqlClient;
using WebApi.Models;

namespace WebApi.Controllers
{
    public class StationController : ApiController
    {
        [HttpGet]
        [EnableCors(origins: "*", headers: "*", methods: "*")]
        public IHttpActionResult station()
        {
            String connetStr = "server=127.0.0.1;port=3306;user=root;password=root; database=zhikexing;";
            MySqlConnection conn = new MySqlConnection(connetStr);
            try
            {
                conn.Open();//建立连接
                string sql = "select * from stations";//查询stations表
                MySqlCommand cmd = new MySqlCommand(sql, conn);
                MySqlDataReader reader = cmd.ExecuteReader();//执行ExecuteReader()返回一个MySqlDataReader对象

                Station stalist = new Station();
                int flag;//判断stalist中是否有当前读取的线路
                while (reader.Read())//初始索引是-1，执行读取下一行数据，返回值是bool
                {
                    flag = 1;

                    //遍历stalist，如果有当前线路，将站点加到该线路中，如果没有，加入该线路
                    foreach(var item in stalist.item)
                    {
                        if((string)reader["s_line"] == item.line_name)
                        {
                            Sta sta = new Sta();
                            sta.sta_name = (string)reader["s_sta_name"];
                            sta.sequence = (int)reader["s_sequence"];
                            item.sta.Add(sta);
                            flag = 0;
                            break;
                        }
                    }
                    if (flag == 1)
                    {
                        Line line = new Line();
                        line.line_name= (string)reader["s_line"];
                        stalist.item.Add(line);
                    }
                }
                //将地铁线路和地铁站进行排序
                stalist.item =stalist.item.OrderBy(e => e.line_name).ToList();
                foreach (var item in stalist.item)
                {
                    item.sta = item.sta.OrderBy(e => e.sequence).ToList();
                }
                //状态码赋值为1
                stalist.status = 1;

                return Json(stalist);
            }
            catch (MySqlException ex)
            {
                return Json(ex.Message);
            }
            finally
            {
                conn.Close();
            }
        }
    }
}
