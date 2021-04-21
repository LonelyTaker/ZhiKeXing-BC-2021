using MySql.Data.MySqlClient;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Web.Http;
using System.Web.Http.Cors;

namespace WebApi.Controllers
{
    public class UserInfoController : ApiController
    {
        [HttpGet]
        [EnableCors(origins: "*", headers: "*", methods: "*")]
        public IHttpActionResult Get()
        {
            String connetStr = "server=127.0.0.1;port=3306;user=root;password=root; database=zhikexing;";
            MySqlConnection conn = new MySqlConnection(connetStr);
            try
            {
                conn.Open();//建立连接
                string sql = "select * from users";
                MySqlCommand cmd = new MySqlCommand(sql, conn);
                MySqlDataReader reader = cmd.ExecuteReader();//执行ExecuteReader()返回一个MySqlDataReader对象
                List<Object> userList = new List<object>();
                if (reader.HasRows)//如果有数据
                {
                    while (reader.Read())//初始索引是-1，执行读取下一行数据，返回值是bool
                    {
                        userList.Add(new
                        {
                            user_id = (string)reader["user_id"],
                            birthyear = reader["u_birthyear"],
                            sex= ((int)reader["u_sex"])==0? "男":"女",
                        });
                    }
                }
                return Json(userList);
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
