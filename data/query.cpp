/*
 * Query.cpp
 *
 *  Created on: May 20, 2014
 *      Author: wang
 */

#include "Query.h"
#include <cmath>
#include <climits>
#include "EncodingConverter.h"
#include "ClientDeal.h"
/*
 * 读取倒排索引到内存中，进行相似度计算
 */
Query::Query(ClientDeal &client, const std::string &invertedfile):client(client),min_str_size("") {
	// TODO Auto-generated constructor stub
	hash_search.clear();
	hash_query.clear() ;
	m_common_query.clear();

	read_to_hash_map(invertedfile); //将倒排索引表中的数据读入到内存中
	run_query(client);
}
/*
 * 加载倒排索引到内存中
 */
void Query::read_to_hash_map(const std::string &invertedfile)
{
	std::ifstream fin ;
	fin.open(invertedfile.c_str());
	if(!fin)
	{
		perror("file open failed");
		exit(1);
	}
	std::string line ;
	int count = 0 ;
	std::string word ;
	std::pair<int, double> tmp ;
	int docid ;
	double inverted ;
	while(getline(fin,line))  //每次读取一行内容
	{
		std::istringstream sin(line);
		sin>>word ;
		while(sin>>docid>>inverted)
		{
			tmp = std::make_pair(docid, inverted);
			hash_search[word].push_back(tmp);
		}
		sin.clear();
	}
	std::cout<<"size is: "<<hash_search.size()<<std::endl;
}
void Query::run_query(ClientDeal &client)
{
	get_query_map(client);
	/*
	 * 求交集
	 */
	count_common_docid();
	int docid = calculate_similarity(client);
	std::cout<<"docid "<<docid<<std::endl;
}
//从倒排索引中获取包含搜索词中的所有集合
void Query::get_query_map(ClientDeal &client)
{
	//GBK存储形式
	std::pair<int, double> tmp ;
	std::string str ;
	int min_size = INT_MAX;  //取最大值
	for(std::map<std::string, std::pair<int, double> >::iterator iter = client.m_word.begin(); iter != client.m_word.end(); ++iter)
	{
		str = iter->first;
		hash_search_iter_const iter = hash_search.find(str);

		if(iter != hash_search.end())  //在hash中找到搜索词所对应的查询结果
		{
			if(min_size > hash_search[str].size())
			{
				min_size = hash_search[str].size();
				min_str_size = str ;   //获取元素集合最小的
			}
			for(std::vector<std::pair<int, double> >::iterator v_iter = hash_search[str].begin();v_iter != hash_search[str].end(); ++v_iter)
			{
				tmp = std::make_pair(v_iter->first, v_iter->second);
				hash_query[str].push_back(tmp);//记录搜索词中的docid和归一化值
			}
		}
	}
	std::cout<<"the size of hash_query is: "<<hash_query.size()<<std::endl;
}
//计算n个集合的公共集合
void Query::count_common_docid()
{
	std::pair<int, double> tmp ;

	//外循环控制寻找次数
	for(std::vector<std::pair<int, double> >::iterator v_iter = hash_query[min_str_size].begin(); v_iter != hash_query[min_str_size].end(); ++v_iter)
	{
		int count = 0;
		hash_search_iter iter = hash_query.begin();
		while(iter != hash_query.end())
		{
			//文章号，关键词， 归一值
			for(std::vector<std::pair<int, double> >::size_type ix = 0;
						ix != hash_query[iter->first].size(); ++ix)
			{
				if(hash_query[iter->first][ix].first == v_iter->first)
				{
					count++ ;
					m_common_query[v_iter->first].push_back(std::make_pair(iter->first,hash_query[iter->first][ix].second));
					break;
				}
			}
			++iter ;
		}
		//表明该下标不是公共集合
		if(count != hash_query.size())
		{
			m_common_iter iter = m_common_query.find(v_iter->first);
			if(iter != m_common_query.end())
			{
				//去除记录
				m_common_query.erase(iter);
			}
		}
	}
}


int Query::calculate_similarity(ClientDeal &client)
{
	m_common_iter m_iter = m_common_query.begin();
	int docid;
	double max_cos_value = 0.0;
	while(m_iter != m_common_query.end())  //遍历文章的docid
	{
		double cos_value = 0.0;
		for(std::vector<std::pair<std::string, double> >::iterator v_iter = m_iter->second.begin(); v_iter != m_iter->second.end(); ++v_iter)
		{
			cos_value += v_iter->second * client.m_word[v_iter->first].second ;  //向量相乘
		}
		if(max_cos_value < cos_value)
		{
			max_cos_value = cos_value ;
			docid = m_iter->first ;
		}
		++m_iter ;
	}
	return docid ;
}
void Query::display()
{
	EncodingConverter trans;
	std::string word;

/*	hash_search_iter hash_iter = hash_query.begin();
	while(hash_iter != hash_query.end())
	{
		word = hash_iter->first ;
		std::cout<<trans.gbkToutf8(word)<<'\t';
		for(std::vector<std::pair<int, double> >::iterator iter = hash_iter->second.begin(); iter != hash_iter->second.end(); ++iter)
		{
			std::cout<<iter->first<<'\t'<<iter->second<<'\t';
		}
		std::cout<<std::endl;
		++hash_iter ;
	}
*/

	m_common_iter iter = m_common_query.begin();
	while(iter != m_common_query.end())
	{
		std::cout<<iter->first<<std::endl;
		for(std::vector<std::pair<std::string, double> >::iterator v_iter = iter->second.begin(); v_iter != iter->second.end(); ++v_iter)
		{
			word = v_iter->first ;
			std::cout<<trans.gbkToutf8(word)<<'\t'<<v_iter->second<<'\t';
		}
		std::cout<<std::endl;
		++iter ;
	}
}
Query::~Query() {
	// TODO Auto-generated destructor stub
}
void Query::write_to_file(const std::string &filename)
{
	std::ofstream fout ;
	fout.open(filename.c_str()) ;
	hash_search_iter iter =  hash_search.begin() ;
	while(iter != hash_search.end())  //将hash_map写入到文件中
	{
		fout<<iter->first<<"   ";
		for(std::vector<std::pair<int, double> >::iterator v_iter = iter->second.begin(); v_iter != iter->second.end(); ++v_iter)
		{
			fout<<v_iter->first<<"   "<<v_iter->second<<"   ";
		}
		fout<<std::endl;
		++iter ;
	}
}
/*
int main(int argc, char **argv)
{
	std::string filename = "/var/www/search_engine/data/inverted_index.dat";
	std::string file = "/var/www/search_engine/data/inverted_test.dat" ;
	Query query(filename);
	//query.write_to_file(file);
	return 0 ;
}
*/