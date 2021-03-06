#ifndef _CAFFEPB_H_
#define _CAFFEPB_H_

// this file is meant to contain functionality that needs the caffe
// protobuf header but not the rest of caffe. thus, boda modes that
// only need this subset of caffe related functionality can function
// without a full caffe install/dependency. also, it should be
// possible to package only the caffe protobuf header and use it here.

#include<string>
#include"conv_util.H" // could use pre-decls instead ...

namespace caffe { class NetParameter; class ConvolutionParameter; }

namespace boda {
  typedef caffe::NetParameter net_param_t;
  typedef shared_ptr< net_param_t > p_net_param_t;

  p_net_param_t must_read_binary_proto( filename_t const & fn, filename_t const & alt_fn );
  p_conv_pipe_t create_pipe_from_param( p_net_param_t const & net_param, map_str_uint32_t const & in_dims, 
					std::string const & out_node_name, bool const & add_bck_ops );
  template< typename CP > void set_param_from_conv_op( CP & cp, p_conv_op_t conv_op );
  void fill_in_conv_op_from_param( p_conv_op_t const & conv_op, caffe::ConvolutionParameter const & cp );
  p_net_param_t parse_and_upgrade_net_param_from_text_file( filename_t const & ptt_fn );
  uint32_t get_layer_ix( net_param_t const & net_param, std::string const & layer_name );

  void create_upsamp_layer_weights( p_conv_pipe_t const & conv_pipe, string const & cpln, 
				    p_conv_pipe_t const & conv_pipe_upsamp, string const & cpuln );

  struct datum_t {
    p_nda_float_t val;
    uint32_t label;
  };
  typedef vector< datum_t > vect_datum_t; 
  typedef shared_ptr< datum_t > p_datum_t; 
  typedef vector< p_datum_t > vect_p_datum_t;

  p_datum_t parse_datum( void const * const bytes, uint32_t const bytes_sz );
  uint32_t parse_datum_into( p_nda_float_t & out, uint32_t const out_ix, void const * const bytes, uint32_t const bytes_sz );
  struct img_t; typedef shared_ptr< img_t > p_img_t; 
  p_img_t datum_to_img( p_datum_t datum );
  void copy_matching_layer_blobs_from_param_to_pipe( p_net_param_t const & blob_src, p_conv_pipe_t const & cp );

}

#endif /* _CAFFEPB_H_ */
